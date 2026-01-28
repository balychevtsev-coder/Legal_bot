from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.google_sheets import GoogleSheetService
import config

gs_service = GoogleSheetService(config.GOOGLE_CREDS_PATH, config.SPREADSHEET_ID)

router = Router()

class Booking(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

# 1. Срабатывает на текстовую кнопку из меню
@router.message(F.text == "📅 Записаться на консультацию")
# 2. Срабатывает на инлайн-кнопку под сообщением ИИ
@router.callback_query(F.data == "start_booking")
async def start_booking(event: types.Message | types.CallbackQuery, state: FSMContext):
    # Определяем, откуда пришло событие, чтобы отправить ответ в нужный чат
    message = event if isinstance(event, types.Message) else event.message
    
    await message.answer("📝 *Начинаем запись.*\nШаг 1 из 2: Как к вам обращаться? (Введите имя)")
    await state.set_state(Booking.waiting_for_name)
    
    # Если это было нажатие инлайн-кнопки, подтверждаем его
    if isinstance(event, types.CallbackQuery):
        await event.answer()

@router.message(Booking.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Шаг 2 из 2: Введите ваш номер телефона для связи:")
    await state.set_state(Booking.waiting_for_phone)

@router.message(Booking.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("name")
    phone = message.text
    
    # Логируем данные в Google Sheets
    try:
        gs_service.log_to_sheets([message.from_user.id, user_name, phone])
        await message.answer(f"✅ *Спасибо, {user_name}!*\nВаша заявка принята. Юрист свяжется с вами по номеру {phone}.")
    except Exception:
        await message.answer("⚠️ Ошибка при сохранении данных в таблицу, но я передам информацию администратору.")
    
    await state.clear()