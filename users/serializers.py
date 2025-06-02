"""
Сериализаторы для пользователей и аутентификации.
Обрабатывают преобразование данных между Python объектами и JSON.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Используется для отображения информации о пользователе.
    """

    # Поле только для чтения - полное имя
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "birth_date",
            "is_verified",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "is_verified")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    Обрабатывает создание нового аккаунта с валидацией пароля.
    """

    # Поля для пароля
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="Пароль должен содержать минимум 8 символов",
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "password",
            "password_confirm",
        )
        extra_kwargs = {
            "email": {"required": True},  # Email обязателен
        }

    def validate(self, attrs):
        """
        Валидация данных регистрации.
        Проверяет совпадение паролей.
        """
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs

    def create(self, validated_data):
        """
        Создание нового пользователя.
        Удаляет поле подтверждения пароля и хеширует пароль.
        """
        # Удаляем поле подтверждения пароля
        validated_data.pop("password_confirm", None)

        # Создаем пользователя с хешированным паролем
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователя.
    Обрабатывает логин по username/email и паролю.
    """

    username = serializers.CharField(help_text="Имя пользователя или email")
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Пароль пользователя",
    )

    def validate(self, attrs):
        """
        Валидация данных для входа.
        Проверяет существование пользователя и правильность пароля.
        """
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # Пытаемся аутентифицировать пользователя
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                # Если аутентификация не удалась, проверяем по email
                try:
                    user_by_email = User.objects.get(email=username)
                    user = authenticate(
                        request=self.context.get("request"),
                        username=user_by_email.username,
                        password=password,
                    )
                except User.DoesNotExist:
                    pass

            if not user:
                raise serializers.ValidationError(
                    "Неверное имя пользователя/email или пароль"
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    "Аккаунт пользователя отключен"
                )

            attrs["user"] = user
            return attrs

        raise serializers.ValidationError(
            "Необходимо указать имя пользователя и пароль"
        )
