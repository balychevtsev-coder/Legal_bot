import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from handlers import common, legal_query, booking

# Функция для настройки экранного меню (кнопка "Меню")
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        types.BotCommand(command="/start", description="🏠 Перезапустить бота"),
        types.BotCommand(command="/help", description="❓ Как пользоваться"),
        types.BotCommand(command="/ask", description="⚖️ Задать вопрос юристу"),
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    logging.basicConfig(level=logging.INFO)

    # Настраиваем Markdown по умолчанию, чтобы не писать это в каждом сообщении
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(common.router)
    dp.include_router(booking.router)
    dp.include_router(legal_query.router)

    # Устанавливаем меню команд при запуске
    await set_main_menu(bot)

    # Пропускаем накопившиеся сообщения и запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")