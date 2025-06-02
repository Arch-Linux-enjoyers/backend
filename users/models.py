"""
Модели для приложения пользователей.
Здесь определяется кастомная модель пользователя с дополнительными полями.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуется от AbstractUser для расширения стандартных возможностей Django.
    """

    # Дополнительные поля пользователя
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Контактный номер телефона пользователя",
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Дата рождения пользователя",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания аккаунта",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления профиля",
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Верифицирован",
        help_text="Подтвержден ли аккаунт пользователя",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "-created_at"
        ]  # Сортировка по дате создания (новые сначала)

    def __str__(self):
        """Строковое представление модели пользователя"""
        return f"{self.username} ({self.email})"

    @property
    def full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
