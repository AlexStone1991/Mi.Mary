import logging
import asyncio
import telegram
from typing import Tuple, List

# Настройка логгера (в основном файле твоего приложения)
logger = logging.getLogger(__name__)

async def send_messages(api_key: str, message: str, *user_ids: str, parse_mode: str = None) -> Tuple[List[str], List[str]]:
    """
    Асинхронно отправляет сообщение пользователям Telegram.

    ID пользователей передаются как отдельные позиционные аргументы (*args) после сообщения.

    Args:
        api_key (str): Токен Telegram бота.
        message (str): Текст сообщения.
        *user_ids (str): Один или несколько ID чатов для отправки.
        parse_mode (str, optional): Режим разметки ('MarkdownV2' или 'HTML').

    Returns:
        Кортеж из двух списков: (список ID, кому успешно отправлено, список ID, кому не удалось отправить).
    """
    bot = telegram.Bot(token=api_key)

    async def _send_single_message(chat_id: str):
        try:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
            logger.info(f"Сообщение успешно отправлено в чат {chat_id}")
            return "success", chat_id
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в чат {chat_id}: {e}")
            return "failure", chat_id

    # user_ids будет кортежем ('id1', 'id2', ...), с которым gather отлично работает
    tasks = [_send_single_message(user_id) for user_id in user_ids]
    results = await asyncio.gather(*tasks)

    successful_ids = [chat_id for status, chat_id in results if status == "success"]
    failed_ids = [chat_id for status, chat_id in results if status == "failure"]
    
    return successful_ids, failed_ids
