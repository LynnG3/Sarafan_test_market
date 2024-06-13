from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, validate_email
from django.db import models

from market_backend.constants import (
    MAX_LENGTH_EMAIL, MAX_LENGTH_STRING_FOR_USER
)
from .validators import validate_username


class CustomUser(AbstractUser):
    """Модель пользователя для приложения."""

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    username = models.CharField(
        verbose_name="Уникальный юзернейм",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        unique=True,
        validators=(
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Имя пользователя содержит недопустимые символы.",
            ),
            validate_username,
        ),
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        validators=(validate_email,),
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"),
                name="unique_user_with_email",
            ),
        ]

    def __str__(self):
        return self.username
