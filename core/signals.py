from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction
import asyncio
import logging

# Импорты из core приложения
from core.models import Review, Order
from core.mistral import is_bad_review
from core.telegram_bot import send_messages

# Импортируем кастомную модель пользователя
from users.models import CustomUser

logger = logging.getLogger(__name__)

api_key = settings.TELEGRAM_BOT_API_KEY
user_id = settings.TELEGRAM_USER_ID
user_id_2 = settings.TELEGRAM_USER_ID_2

@receiver(m2m_changed, sender=Order.services.through)
def notify_telegram_on_order_create(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    """
    try:
        if action == 'post_add' and kwargs.get('pk_set'):
            logger.info(f"📦 Обнаружен новый заказ: {instance.id}")
            transaction.on_commit(lambda: send_order_notification(instance))
    except Exception as e:
        logger.error(f"❌ Ошибка в обработчике заказа: {e}")

def send_order_notification(instance):
    """Функция для отправки уведомления о заказе"""
    try:
        list_services = [service.name for service in instance.services.all()]
        appointment_date = instance.appointment_date.strftime("%d.%m.%Y") if instance.appointment_date else "Не указана"
        tg_markdown_message = f"""
======Новый заказ!======
Имя: {instance.client_name}
Телефон: {instance.phone}
Дата записи: {appointment_date}
Услуги: {', '.join(list_services)}
Комментарий: {instance.comment}
Подробнее: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
#заказ
"""
        asyncio.run(send_messages(api_key, tg_markdown_message, user_id, user_id_2))
        logger.info(f"✅ Уведомление о заказе {instance.id} отправлено в Telegram")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки сообщения в Telegram: {e}")

@receiver(post_save, sender=Review)
def handle_new_review(sender, instance, created, **kwargs):
    """
    Основной обработчик для новых отзывов.
    """
    if created and not kwargs.get('raw', False):
        logger.info(f"💬 Обнаружен новый отзыв: {instance.id}")
        transaction.on_commit(lambda: process_review(instance))

def process_review(instance):
    """
    Асинхронная обработка отзыва: модерация + уведомление
    """
    try:
        logger.info(f"🔄 Начинаем обработку отзыва {instance.id}")
        
        # Обновляем статус на модерации
        Review.objects.filter(id=instance.id).update(status="ai_moderating")
        logger.info(f"📊 Статус отзыва {instance.id} изменен на ai_moderating")
        
        # Запускаем валидацию через AI
        is_bad = is_bad_review(instance.text)
        logger.info(f"🤖 Результат модерации отзыва {instance.id}: {'bad' if is_bad else 'good'}")
        
        if is_bad:
            # Отзыв плохой - отклоняем
            Review.objects.filter(id=instance.id).update(
                status="ai_rejected", 
                is_published=False
            )
            logger.info(f"❌ Отзыв {instance.id} отклонен")
        else:
            # Отзыв хороший - одобряем и публикуем
            Review.objects.filter(id=instance.id).update(
                status="ai_approved", 
                is_published=True  # ПРАВИЛЬНОЕ имя поля!
            )
            logger.info(f"✅ Отзыв {instance.id} одобрен и опубликован")
        
        # Перезагружаем instance с обновленными данными
        updated_instance = Review.objects.get(id=instance.id)
        
        # Отправляем уведомление
        send_review_notification(updated_instance)
        
    except Exception as e:
        logger.error(f"💥 Ошибка при обработке отзыва {instance.id}: {e}")
        # В случае ошибки возвращаем в исходное состояние
        Review.objects.filter(id=instance.id).update(status="ai_moderating")

def send_review_notification(instance):
    """Функция для отправки уведомления об отзыве"""
    try:
        status_emoji = "✅" if instance.status == "ai_approved" else "❌" if instance.status == "ai_rejected" else "⏳"
        publication_status = "ОПУБЛИКОВАН" if instance.is_published else "НЕ ОПУБЛИКОВАН"
        
        tg_plain_message = f"""
=== НОВЫЙ ОТЗЫВ! {status_emoji} ===
Имя: {instance.client_name}
Рейтинг: {instance.rating} ⭐
Статус: {instance.get_status_display()}
Публикация: {publication_status}
Текст: {instance.text[:200]}{'...' if len(instance.text) > 200 else ''}
Подробнее: http://127.0.0.1:8000/admin/core/review/{instance.id}/change/
#отзыв #{instance.status}
"""
        asyncio.run(send_messages(api_key, tg_plain_message, user_id, user_id_2, None))
        logger.info(f"📨 Уведомление об отзыве {instance.id} отправлено в Telegram")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки сообщения в Telegram: {e}")



@receiver(post_save, sender=CustomUser)
def notify_telegram_on_user_create(sender, instance, created, **kwargs):
    """
    Обработчик сигнала post_save для модели CustomUser.
    """
    if created and not kwargs.get('raw', False):
        logger.info(f"👤 Обнаружен новый пользователь: {instance.id}")
        transaction.on_commit(lambda: send_user_notification(instance))

def send_user_notification(instance):
    """Функция для отправки уведомления о пользователе"""
    try:
        tg_markdown_message = f"""
=== Новый пользователь! ===
Имя пользователя: {instance.username}
Email: {instance.email if instance.email else 'Не указан'}
Дата регистрации: {instance.date_joined.strftime("%d.%m.%Y %H:%M")}
Подробнее: http://127.0.0.1:8000/admin/users/customuser/{instance.id}/change/
#пользователь
"""
        asyncio.run(send_messages(tg_markdown_message, api_key, user_id, user_id_2))
        logger.info(f"✅ Уведомление о пользователе {instance.id} отправлено в Telegram")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки сообщения в Telegram: {e}")