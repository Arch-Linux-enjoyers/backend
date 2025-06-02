"""
Настройки админки для модели пользователя.
Настраивает отображение пользователей в Django admin.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Кастомная админка для модели User.
    Расширяет стандартную админку Django дополнительными полями.
    """

    # Поля для отображения в списке пользователей
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    # Поля для поиска
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )

    # Фильтры в правой панели
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "date_joined",
        "created_at",
    )

    # Поля только для чтения
    readonly_fields = ("created_at", "updated_at", "date_joined", "last_login")

    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "birth_date",
                )
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Важные даты",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Поля для формы добавления нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Сортировка по умолчанию
    ordering = ("-created_at",)
