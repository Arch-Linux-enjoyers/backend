# Django MAI - API проект с аутентификацией

Django REST Framework проект с кастомной моделью пользователя, аутентификацией и Docker поддержкой.

## 🚀 Особенности

- **Django 4.2** с **Django REST Framework**
- **Кастомная модель пользователя** с дополнительными полями
- **API для аутентификации** (регистрация, вход, выход)
- **PostgreSQL** база данных
- **Docker Compose** для развертывания
- **Nginx** веб-сервер с проксированием
- **Poetry** для управления зависимостями
- Полное **покрытие комментариями** кода

## 📋 Требования

- Docker и Docker Compose
- Python 3.10+ (для локальной разработки)
- Poetry (для локальной разработки)

## 🔧 Установка и запуск

### Быстрый старт с Docker

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd django-mai
```

2. **Скопируйте файл с переменными окружения:**
```bash
cp environment.env .env
```

3. **Отредактируйте .env файл** (установите свои значения):
```bash
# Django настройки
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# База данных PostgreSQL
DB_NAME=django_mai_db
DB_USER=postgres
DB_PASSWORD=strong_password_here
DB_HOST=db
DB_PORT=5432

# Настройки для Docker
POSTGRES_DB=django_mai_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=strong_password_here
```

4. **Запустите приложение:**
```bash
docker-compose up -d --build
```

5. **Проверьте статус сервисов:**
```bash
docker-compose ps
```

### Локальная разработка

1. **Установите зависимости:**
```bash
poetry install
```

2. **Активируйте виртуальное окружение:**
```bash
poetry shell
```

3. **Примените миграции:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

5. **Запустите сервер разработки:**
```bash
python manage.py runserver
```

## 📚 API Endpoints

### Аутентификация

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `POST` | `/api/users/register/` | Регистрация нового пользователя | Не требуется |
| `POST` | `/api/users/login/` | Вход в систему | Не требуется |
| `POST` | `/api/users/logout/` | Выход из системы | Требуется |
| `GET` | `/api/users/auth-status/` | Проверка статуса аутентификации | Не требуется |

### Профиль пользователя

| Метод | URL | Описание | Авторизация |
|-------|-----|----------|-------------|
| `GET` | `/api/users/profile/` | Получение профиля | Требуется |
| `PUT/PATCH` | `/api/users/profile/update/` | Обновление профиля | Требуется |

### Примеры запросов

**Регистрация пользователя:**
```bash
curl -X POST http://localhost/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Имя",
    "last_name": "Фамилия"
  }'
```

**Вход в систему:**
```bash
curl -X POST http://localhost/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

## 🗄️ Модель пользователя

Кастомная модель User расширяет стандартную модель Django дополнительными полями:

- `phone_number` - номер телефона
- `birth_date` - дата рождения  
- `created_at` - дата создания аккаунта
- `updated_at` - дата последнего обновления
- `is_verified` - статус верификации

## 🐳 Docker структура

- **web** - Django приложение (порт 8000)
- **db** - PostgreSQL база данных (порт 5432)
- **nginx** - веб-сервер (порт 80)

### Volumes

- `postgres_data` - данные PostgreSQL
- `static_volume` - статические файлы Django
- `media_volume` - загружаемые файлы

### Сеть

- `django_network` - изолированная сеть для всех сервисов

## 🔍 Полезные команды

**Просмотр логов:**
```bash
docker-compose logs -f web    # Логи Django
docker-compose logs -f db     # Логи PostgreSQL
docker-compose logs -f nginx  # Логи Nginx
```

**Выполнение команд Django:**
```bash
docker-compose exec web poetry run python manage.py shell
docker-compose exec web poetry run python manage.py makemigrations
docker-compose exec web poetry run python manage.py migrate
```

**Подключение к базе данных:**
```bash
docker-compose exec db psql -U postgres -d django_mai_db
```

**Остановка и удаление:**
```bash
docker-compose down              # Остановка
docker-compose down -v           # Остановка с удалением volumes
docker-compose down --rmi all    # Остановка с удалением образов
```

## 🛡️ Безопасность

- Все пароли и секретные ключи вынесены в переменные окружения
- Настроены заголовки безопасности в Nginx
- Используется пользователь без прав root в Docker контейнере
- Настроена изолированная Docker сеть

## 📝 Структура проекта

```
django-mai/
├── django_mai/          # Основной Django проект
│   ├── settings.py      # Настройки проекта
│   ├── urls.py          # URL маршруты
│   └── wsgi.py          # WSGI конфигурация
├── users/               # Приложение пользователей
│   ├── models.py        # Модели данных
│   ├── views.py         # API views
│   ├── serializers.py   # DRF сериализаторы
│   ├── admin.py         # Админка
│   └── urls.py          # URL маршруты
├── nginx/               # Конфигурация Nginx
│   ├── nginx.conf       # Основная конфигурация
│   └── default.conf     # Конфигурация виртуального хоста
├── Dockerfile           # Docker образ для Django
├── docker-compose.yml   # Docker Compose конфигурация
├── pyproject.toml       # Poetry зависимости
├── entrypoint.sh        # Скрипт запуска
└── environment.env      # Переменные окружения (пример)
```

## 🤝 Разработка

1. Создайте новую ветку для ваших изменений
2. Внесите изменения и добавьте комментарии
3. Протестируйте изменения локально
4. Создайте Pull Request

## 📄 Лицензия

Этот проект создан в учебных целях. 