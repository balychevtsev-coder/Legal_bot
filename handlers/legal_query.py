from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.openai_service import get_legal_answer, create_thread

router = Router()
user_threads = {}

booking_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Записаться на консультацию", callback_data="start_booking")]
])

# Обработка нажатия кнопки "Задать вопрос юристу"
@router.message(F.text == "⚖️ Задать вопрос юристу")
async def ask_instruction(message: types.Message):
    await message.answer(
        "🤝 Я готов! Напишите ваш вопрос по налогам или регистрации бизнеса прямо в чат.\n\n"
        "*Например:* «Как ИП перейти на патент в 2026 году?»"
    )

# Основной обработчик (Catch-all), который шлет вопросы в OpenAI
@router.message(F.text)
async def handle_questions(message: types.Message):
    user_id = message.from_user.id
    
    # Игнорируем другие кнопки меню, если они вдруг попали сюда
    if message.text in ["📅 Записаться на консультацию", "ℹ️ О сервисе"]:
        return

    if user_id not in user_threads:
        user_threads[user_id] = await create_thread()
    
    wait_msg = await message.answer("🔍 *Анализирую вопрос...*")
    
    # Статус "печатает" для реалистичности
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        answer = await get_legal_answer(user_threads[user_id], message.text)
        await wait_msg.delete()
        
        await message.answer(
            answer,
            reply_markup=booking_kb # Оставляем инлайн-кнопку под ответом ИИ
        )
    except Exception as e:
        await wait_msg.edit_text("❌ Произошла ошибка при связи с ИИ-ассистентом.")
        print(f"Error: {e}")