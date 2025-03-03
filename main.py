from aiogram import Bot, Dispatcher
import logging
from asyncio import run
from aiogram.types import BotCommand

# db 
from database.model import main_db_create

# routers
from routers.startRouter import startRouter
from routers.adminRouter import adminrouter
from routers.userRouter import userRouter

async def set_botCommands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni Ishga tushirish" ),
        BotCommand(command="/help", description="Yordam" ),
    ]

    await bot.set_my_commands(commands)
async def main():
    bot = Bot(token="7917367014:AAGPpRuiR5G11F5FMGg32JRQN9zcmhNOsxw")
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    # router
    await set_botCommands(bot)
    dp.include_router(startRouter)
    dp.include_router(adminrouter)
    dp.include_router(userRouter)

    await main_db_create()
    await dp.start_polling(bot)

if __name__=="__main__":
    try:
        run(main())
    except KeyboardInterrupt:
        print("Bot ishi yakunlandi")