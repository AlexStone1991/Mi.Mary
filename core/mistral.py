# импорт из настроек MISTRAL_MODERATIONS_GRADES
from mi_mary.settings import MISTRAL_MODERATIONS_GRADES, MISTRAL_API_KEY
import os
from dotenv import load_dotenv
from mistralai import Mistral
from pprint import pprint
import time
import logging

logger = logging.getLogger(__name__)

def is_bad_review(review_text: str, api_key: str = MISTRAL_API_KEY, grades: dict = MISTRAL_MODERATIONS_GRADES) -> bool:
    """
    Проверяет отзыв на наличие запрещенного контента через Mistral AI.
    Возвращает True если отзыв содержит запрещенный контент.
    """
    if not api_key:
        logger.error("MISTRAL_API_KEY не настроен")
        return False
    
    if not review_text or not review_text.strip():
        logger.warning("Пустой текст отзыва")
        return False
    
    try:
        # Создаем клиента Mistral с переданным API ключом
        client = Mistral(api_key=api_key)

        # Формируем запрос
        response = client.classifiers.moderate_chat(
            model="mistral-moderation-latest",
            inputs=[{"role": "user", "content": review_text}],
        )
        
        # Вытаскиваем данные с оценкой
        result = response.results[0].category_scores

        # Округляем значения до двух знаков после запятой
        result = {key: round(value, 3) for key, value in result.items()}

        logger.info(f"Результат модерации отзыва: {result}")

        # Словарь под результаты проверки
        checked_result = {}

        for key, value in result.items():
            if key in grades:
                checked_result[key] = value >= grades[key]

        # Если одно из значений True, то отзыв не проходит модерацию
        is_bad = any(checked_result.values())
        
        logger.info(f"Отзыв {'не прошел' if is_bad else 'прошел'} модерацию")
        
        # тестовый слип 2 секунды (уменьшил для скорости)
        time.sleep(2)
        
        return is_bad
        
    except Exception as e:
        logger.error(f"Ошибка при модерации отзыва: {e}")
        # В случае ошибки считаем отзыв безопасным (чтобы не блокировать работу)
        return False