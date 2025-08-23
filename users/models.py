from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avarars", verbose_name="Аватар", null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=20, null=True, blank=True)
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    vk_id = models.CharField(max_length=100, verbose_name="ID ВКонтакте", null=True, blank=True)
    tg_id = models.CharField(max_length=100, verbose_name="ID Telegram", null=True, blank=True)
