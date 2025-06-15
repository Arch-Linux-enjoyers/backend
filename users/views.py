'''
Views для аутентификации и управления пользователями.

Содержит API endpoints для регистрации, входа, выхода и получения профиля.
'''

from django.conf import settings as django_settings
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from django.utils.cache import patch_vary_headers
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


@api_view(['GET'])
def get_csrf_cookie(request: Request) -> Response:
    '''API for getting an CSRF token for other API requests.'''
    response = Response({'csrfToken': get_token(request)})
    response.set_cookie(
        django_settings.CSRF_COOKIE_NAME,
        request.META['CSRF_COOKIE'],
        max_age=django_settings.CSRF_COOKIE_AGE,
        domain=django_settings.CSRF_COOKIE_DOMAIN,
        path=django_settings.CSRF_COOKIE_PATH,
        secure=django_settings.CSRF_COOKIE_SECURE,
        httponly=django_settings.CSRF_COOKIE_HTTPONLY,
        samesite=django_settings.CSRF_COOKIE_SAMESITE,
    )
    # Set the Vary header since content varies with the CSRF cookie.
    patch_vary_headers(response, ('Cookie',))
    return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request: Request) -> Response:
    '''
    API endpoint для регистрации нового пользователя.

    Принимает POST запрос с данными пользователя:
    - username: имя пользователя
    - email: email адрес
    - password: пароль
    - password_confirm: подтверждение пароля
    - first_name: имя (опционально)
    - last_name: фамилия (опционально)
    - phone_number: номер телефона (опционально)
    - birth_date: дата рождения (опционально)
    '''
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Автоматически входим пользователя после регистрации
        login(request, user)

        # Возвращаем данные созданного пользователя
        user_serializer = UserSerializer(user)

        return Response(
            {
                'message': 'Пользователь успешно зарегистрирован',
                'user': user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'message': 'Ошибка при регистрации', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request: Request) -> Response:
    '''
    API endpoint для входа пользователя в систему.

    Принимает POST запрос с данными:
    - username: имя пользователя или email
    - password: пароль
    '''
    print('view')
    serializer = LoginSerializer(
        data=request.data, context={'request': request}
    )

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Входим пользователя в систему
        login(request, user)

        # Возвращаем данные пользователя
        user_serializer = UserSerializer(user)

        return Response(
            {
                'message': 'Успешный вход в систему',
                'user': user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {'message': 'Ошибка при входе', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request: Request) -> Response:
    '''
    API endpoint для выхода пользователя из системы.

    Требует аутентификации. Завершает сессию пользователя.
    '''
    # try:
    # Выходим пользователя из системы
    logout(request)

    return Response(
        {'message': 'Успешный выход из системы'}, status=status.HTTP_200_OK
    )

    # except Exception as e:
    #     return Response(
    #         {'message': 'Ошибка при выходе из системы', 'error': str(e)},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request: Request) -> Response:
    '''
    API endpoint для получения профиля текущего пользователя.

    Требует аутентификации. Возвращает данные профиля пользователя.
    '''
    user = request.user
    serializer = UserSerializer(user)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )

    # except Exception as e:
    #     return Response(
    #         {'message': 'Ошибка при получении профиля', 'error': str(e)},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request: Request) -> Response:
    '''
    API endpoint для обновления профиля пользователя.

    Требует аутентификации. Принимает PUT/PATCH запрос с данными для обновления:
    - first_name: имя
    - last_name: фамилия
    - email: email адрес
    - phone_number: номер телефона
    - birth_date: дата рождения
    '''
    # try:
    user = request.user

    # Используем partial=True для PATCH запросов (частичное обновление)
    partial = request.method == 'PATCH'

    serializer = UserSerializer(user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            'message': 'Ошибка при обновлении профиля',
            'errors': serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )

    # except Exception as e:
    #     return Response(
    #         {'message': 'Ошибка при обновлении профиля', 'error': str(e)},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def auth_status_view(request: Request) -> Response:
    '''
    API endpoint для проверки статуса аутентификации.

    Возвращает информацию о том, аутентифицирован ли пользователь.
    Если да - возвращает данные пользователя.
    '''
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(
            {'is_authenticated': True, 'user': serializer.data},
            status=status.HTTP_200_OK,
        )

    return Response(
        {'is_authenticated': False, 'user': None}, status=status.HTTP_200_OK
    )
