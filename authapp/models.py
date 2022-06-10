from django.contrib.auth.models import AbstractUser
from django.db import models
from mainapp.models import NULLABLE
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name=_("email"), unique=True)
    age = models.PositiveSmallIntegerField(verbose_name=_("age"), **NULLABLE)
    avatar = models.ImageField(upload_to="users", verbose_name=_("avatar"), **NULLABLE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
