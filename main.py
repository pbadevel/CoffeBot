# from aiogram import Bot, Dispatcher
# from aiogram.client.default import DefaultBotProperties
from aiogram.types import ErrorEvent, FSInputFile
import traceback

import logging as lg
from settings import config
import asyncio



from handlers import admin_handler, user_handler


# testimageid: AgACAgQAAxkBAAIBUmgepvOdW8eKStDcirfnZtKOY98bAALhxDEbsST4UDhSxmDukigqAQADAgADeQADNgQ

async def main():

    config.dp.include_router(admin_handler.router)
    config.dp.include_router(user_handler.router)

    print(config.ADMIN_IDS)
    
    @config.dp.error()
    async def error_handler(event: ErrorEvent):
        lg.critical("Критическая ошибка: %s", event.exception, exc_info=True)
        await config.bot.send_message(chat_id=1060834219,
                               text=f'{event.exception}')
        
        formatted_lines = traceback.format_exc()
        text_file = open('error.txt', 'w')
        text_file.write(str(formatted_lines))
        text_file.close()
        await config.bot.send_document(chat_id=1060834219,
                                document=FSInputFile('error.txt'))
            
    await config.dp.start_polling(config.bot)

if __name__ == "__main__":
    lg.basicConfig(level=lg.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")


