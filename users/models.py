from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", **NULLABLE)
    phone_number = models.CharField(
        max_length=20, verbose_name="Номер телефона", **NULLABLE, help_text="Введите номер телефона"
    )
    country = CountryField(max_length=50, blank_label="(выберите страну)", **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars", **NULLABLE, verbose_name="Аватар")
    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Возможность блокировки пользователя"),
        ]
