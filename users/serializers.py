'''
Сериализаторы для пользователей и аутентификации.

Обрабатывают преобразование данных между Python объектами и JSON.
'''

from django.contrib.auth import authenticate
from rest_framework import serializers

from . import exceptions
from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели пользователя.

    Используется для отображения информации о пользователе.
    '''

    class Meta:  # noqa: D106
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'is_verified')
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_verified')


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для регистрации нового пользователя.

    Обрабатывает создание нового аккаунта с валидацией пароля.
    '''

    # Поля для пароля
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text='Пароль должен содержать минимум 8 символов',
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Подтверждение пароля',
    )

    class Meta:  # noqa: D106
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'password',
            'password_confirm',
        )
        extra_kwargs = {
            'email': {'required': True},  # Email обязателен
        }

    def validate(self, attrs: dict) -> dict:
        '''
        Валидация данных регистрации.

        Проверяет совпадение паролей.
        '''
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise exceptions.PasswordsDontMatchError

        return attrs

    def create(self, validated_data: dict) -> type[User]:
        '''
        Создание нового пользователя.

        Удаляет поле подтверждения пароля и хеширует пароль.
        '''
        # Удаляем поле подтверждения пароля
        validated_data.pop('password_confirm', None)

        # Создаем пользователя с хешированным паролем  # noqa: RUF003
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    '''
    Сериализатор для аутентификации пользователя.

    Обрабатывает логин по username/email и паролю.
    '''

    username = serializers.CharField(help_text='Имя пользователя или email')
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Пароль пользователя',
    )

    def validate(self, attrs: dict) -> dict:
        '''
        Валидация данных для входа.

        Проверяет существование пользователя и правильность пароля.
        '''
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Пытаемся аутентифицировать пользователя
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password,
            )

            if not user:
                # Если аутентификация не удалась, проверяем по email
                try:
                    user_by_email = User.objects.get(email=username)
                    user = authenticate(
                        request=self.context.get('request'),
                        username=user_by_email.username,
                        password=password,
                    )
                except User.DoesNotExist:
                    pass

            if not user:
                raise exceptions.InvalidLoginOrPasswordError

            if not user.is_active:
                raise exceptions.UserAccountDeactivatedError

            attrs['user'] = user
            return attrs

        raise exceptions.UsernameOrPasswordDontProvidedError
