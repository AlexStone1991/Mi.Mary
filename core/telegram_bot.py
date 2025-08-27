import logging
import telegram
# import os
# import asyncio
# from dotenv import load_dotenv

# load_dotenv()


# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

async def send_telegram_message(token, chat_id, message, parse_mode="Markdown"):
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
        logging.info(f'Сообщение "{message}" отправлено в чат {chat_id}')
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения в чат {chat_id}: {e}")
        raise

# if __name__ == "__main__":
#     load_dotenv()
#     TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
#     TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
#     message = "Текстовое сообщение"
#     asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))