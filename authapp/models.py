from django.contrib.auth.models import AbstractUser
from django.db import models
from mainapp.models import NULLABLE


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name="Email", unique=True)
    age = models.PositiveSmallIntegerField(verbose_name="Возраст", **NULLABLE)
    avatar = models.ImageField(upload_to="users", **NULLABLE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



