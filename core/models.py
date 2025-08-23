from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", verbose_name="Изображение", null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ("confirmed", "Подтвержден"),
        ("completed", "Завершена"),
        ("canceled", "Отменена"),
    )
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    services = models.ManyToManyField(Service, related_name="orders", verbose_name="Услуги")
    appointment_date = models.DateField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ {self.id} - {self.client_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    )

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("ai_moderating", "На модерации"),
        ("ai_approved", "Одобрен"),
        ("ai_rejected", "Отклонен"),
        ("published", "Опубликован"),
        ("archived", "В архиве"),
    ]
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    photo = models.ImageField(upload_to="reviews/", verbose_name="Фотография", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус")

    def __str__(self):
        return f"Отзыв {self.id} - {self.client_name}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']