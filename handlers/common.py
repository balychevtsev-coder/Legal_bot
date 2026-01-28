from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from services.google_sheets import GoogleSheetService # Импортируем КЛАСС
import config

router = Router()

gs_service = GoogleSheetService(config.GOOGLE_CREDS_PATH, config.SPREADSHEET_ID)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем строитель клавиатуры
    builder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки (в ряд или по одной)
    builder.row(types.KeyboardButton(text="⚖️ Задать вопрос юристу"))
    builder.row(
        types.KeyboardButton(text="📅 Записаться на консультацию"),
        types.KeyboardButton(text="❓ FAQ")
    )
    builder.row(types.KeyboardButton(text="ℹ️ О сервисе"))
    
    # Формируем клавиатуру с параметром resize_keyboard (чтобы кнопки были компактными)
    main_kb = builder.as_markup(resize_keyboard=True)

    await message.answer(
        f"👋 Приветствую, {message.from_user.first_name}!\n\n"
        "Я ваш интеллектуальный помощник по налогам и регистрации бизнеса.\n"
        "Выберите действие в меню ниже или просто задайте свой вопрос.",
        reply_markup=main_kb
    )

# --- ЛОГИКА FAQ ---

@router.message(F.text == "❓ FAQ")
async def show_faq(message: types.Message):
    # Используем метод класса
    faq_items = gs_service.get_faq_data()
    
    if not faq_items:
        await message.answer("Раздел FAQ дополняется. Загляните позже!")
        return

    builder = InlineKeyboardBuilder()
    for index, item in enumerate(faq_items):
        # Делаем текст кнопки коротким
        txt = item['Вопрос'][:40] + "..." if len(item['Вопрос']) > 40 else item['Вопрос']
        builder.row(types.InlineKeyboardButton(text=txt, callback_data=f"faq_{index}"))
    
    await message.answer("📚 *Часто задаваемые вопросы:*", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("faq_"))
async def faq_answer(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    faq_items = gs_service.get_faq_data()
    
    if index < len(faq_items):
        item = faq_items[index]
        await callback.message.answer(f"❓ *{item['Вопрос']}*\n\n✅ {item['Ответ']}")
    await callback.answer()

@router.message(Command("help"))
@router.message(lambda message: message.text == "ℹ️ О сервисе") # Обработка и команды, и кнопки
async def cmd_help(message: types.Message):
    help_text = (
        "📖 *Как я работаю:*\n\n"
        "1. *Консультация:* Просто напишите свой вопрос в чат. Я использую базу знаний законов РФ.\n"
        "2. *Запись:* Если ИИ недостаточно, нажмите кнопку записи к живому юристу.\n"
        "3. *Точность:* Я всегда стараюсь указывать статьи НК РФ."
    )
    await message.answer(help_text)