from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
import asyncio

# Импорты из core приложения
from core.models import Review, Order
from core.mistral import is_bad_review
from core.telegram_bot import send_telegram_message

# Импортируем кастомную модель пользователя
from users.models import CustomUser

api_key = settings.TELEGRAM_BOT_API_KEY
user_id = settings.TELEGRAM_USER_ID

@receiver(m2m_changed, sender=Order.services.through)
def notify_telegram_on_order_create(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на консультацию.
    """
    try:
        if action == 'post_add' and kwargs.get('pk_set'):
            # Добавляем небольшую задержку для гарантии сохранения данных
            from django.db import transaction
            transaction.on_commit(lambda: send_order_notification(instance))
    except Exception as e:
        print(f"Ошибка в обработчике заказа: {e}")

def send_order_notification(instance):
    """Функция для отправки уведомления о заказе"""
    try:
        list_services = [service.name for service in instance.services.all()]
        appointment_date = instance.appointment_date.strftime("%d.%m.%Y") if instance.appointment_date else "Не указана"
        tg_markdown_message = f"""
====== *Новый заказ!* ======
**Имя:** {instance.client_name}
**Телефон:** {instance.phone}
**Дата записи:** {appointment_date}
**Услуги:** {', '.join(list_services)}
**Комментарий:** {instance.comment}
**Подробнее:** http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
#заказ
"""
        asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

@receiver(post_save, sender=Review)
def process_review_and_notify(sender, instance, created, **kwargs):
    """
    Комбинированный обработчик для отзывов:
    - AI модерация
    - Авто-публикация
    - Отправка уведомления
    """
    if created and not kwargs.get('raw', False):
        try:
            # Меняем статус "На модерации"
            instance.status = "ai_moderating"
            instance.save(update_fields=['status'])
            
            # Запускаем валидацию через AI
            is_bad = is_bad_review(instance.text)
            
            if is_bad:
                instance.status = "ai_rejected"
                instance.is_published = False
            else:
                instance.status = "ai_approved"
                instance.is_published = True  # Автоматически публикуем хороший отзыв
            
            instance.save(update_fields=['status', 'is_published'])
            
            # Отправляем уведомление после модерации
            send_review_notification(instance)
            
        except Exception as e:
            print(f"Ошибка при обработке отзыва: {e}")
            # В случае ошибки оставляем на модерации
            instance.status = "ai_moderating"
            instance.save(update_fields=['status'])

def send_review_notification(instance):
    """Функция для отправки уведомления об отзыве"""
    try:
        status_emoji = "✅" if instance.status == "ai_approved" else "❌" if instance.status == "ai_rejected" else "⏳"
        publication_status = "ОПУБЛИКОВАН" if instance.is_published else "НЕ ОПУБЛИКОВАН"
        
        tg_markdown_message = f"""
====== *Новый отзыв!* {status_emoji} ======
**Имя:** {instance.client_name}
**Рейтинг:** {instance.rating} ⭐
**Статус:** {instance.get_status_display()}
**Публикация:** {publication_status}
**Текст:** {instance.text[:200]}{'...' if len(instance.text) > 200 else ''}
**Подробнее:** http://127.0.0.1:8000/admin/core/review/{instance.id}/change/
#отзыв #{instance.status}
"""
        asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

@receiver(post_save, sender=CustomUser)
def notify_telegram_on_user_create(sender, instance, created, **kwargs):
    """
    Обработчик сигнала post_save для модели CustomUser.
    Отправляет уведомление в Telegram о новом пользователе.
    """
    if created and not kwargs.get('raw', False):
        try:
            # Добавляем задержку для гарантии сохранения
            from django.db import transaction
            transaction.on_commit(lambda: send_user_notification(instance))
        except Exception as e:
            print(f"Ошибка в обработчике пользователя: {e}")

def send_user_notification(instance):
    """Функция для отправки уведомления о пользователе"""
    try:
        tg_markdown_message = f"""
====== *Новый пользователь!* ======
**Имя пользователя:** {instance.username}
**Email:** {instance.email if instance.email else 'Не указан'}
**Дата регистрации:** {instance.date_joined.strftime("%d.%m.%Y %H:%M")}
**Подробнее:** http://127.0.0.1:8000/admin/users/customuser/{instance.id}/change/
#пользователь
"""
        asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")