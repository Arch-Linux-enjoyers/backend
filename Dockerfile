# Используем официальный Python образ в качестве базового
FROM python:3.10-slim

# Устанавливаем переменные окружения
# PYTHONDONTWRITEBYTECODE - предотвращает создание .pyc файлов
# PYTHONUNBUFFERED - выводит логи сразу, не буферизирует их
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Устанавливаем системные зависимости
# postgresql-client - для работы с PostgreSQL
# build-essential - для компиляции Python пакетов
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Настраиваем Poetry
# Отключаем создание виртуального окружения (используем контейнер)
ENV POETRY_VENV_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы Poetry для установки зависимостей
COPY pyproject.toml ./

# Устанавливаем зависимости
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Копируем весь проект
COPY . .

# Создаем директории для статических и медиа файлов
RUN mkdir -p /app/staticfiles /app/media

# Создаем пользователя для запуска приложения (безопасность)
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Открываем порт 8000
EXPOSE 8000

# Создаем скрипт для запуска приложения
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Команда запуска приложения
ENTRYPOINT ["/app/entrypoint.sh"] 