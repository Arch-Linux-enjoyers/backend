'''
URL маршруты для приложения пользователей.

Определяет endpoints для аутентификации и управления профилем.
'''


from django.urls import path

from . import views


urlpatterns = [
    # Эндпоинт для регистрации нового пользователя
    # POST /api/users/register/
    path('register/', views.register_view, name='register'),
    # Эндпоинт для входа в систему
    # POST /api/users/login/
    path('login/', views.login_view, name='login'),
    # Эндпоинт для выхода из системы
    # POST /api/users/logout/
    path('logout/', views.logout_view, name='logout'),
    # Эндпоинт для получения профиля текущего пользователя
    # GET /api/users/profile/
    path('profile/', views.profile_view, name='profile'),
    # Эндпоинт для обновления профиля пользователя
    # PUT, PATCH /api/users/profile/update/
    path('profile/update/', views.update_profile_view, name='update_profile'),
    # Эндпоинт для проверки статуса аутентификации
    # GET /api/users/auth-status/
    path('auth-status/', views.auth_status_view, name='auth_status'),
]
