#!/bin/sh
# Скрипт запуска Django приложения
# Выполняет миграции и запускает сервер

set -e  # Останавливаем выполнение при любой ошибке

echo "🚀 Запуск Django приложения..."

# Простое ожидание доступности базы данных
echo "⏳ Ожидание доступности базы данных..."
while ! pg_isready -h db -p 5432 -U ${DB_USER:-postgres} > /dev/null 2>&1; do
    echo "База данных недоступна, ожидаем 2 секунды..."
    sleep 2
done
echo "✅ База данных доступна!"

# Выполняем миграции базы данных
echo "📊 Выполнение миграций базы данных..."
python manage.py makemigrations
python manage.py migrate

# Собираем статические файлы для продакшена
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput

# Создаем суперпользователя если его нет (для первого запуска)
echo "👤 Проверка суперпользователя..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    print('Создание суперпользователя...');
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Суперпользователь создан: admin/admin123');
else:
    print('Суперпользователь уже существует');
"

echo "✅ Инициализация завершена!"

# Запускаем сервер
if [ "$DEBUG" = "True" ]; then
    echo "🔧 Запуск в режиме разработки..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "🏭 Запуск в продакшен режиме..."
    gunicorn django_mai.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi