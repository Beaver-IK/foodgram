# Foodgram - Кулинарная Социальная Сеть

![Foodgram](https://img.shields.io/badge/status-active-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.9-blue) 
![Django](https://img.shields.io/badge/Django-4.2-green) 
![React](https://img.shields.io/badge/React-18-blue) 
![Docker](https://img.shields.io/badge/Docker-20.10-blue) 
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue)

## Описание проекта
Foodgram - это веб-сайт, где пользователи могут делиться своими кулинарными рецептами, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям доступен сервис "Список покупок", который позволяет создавать список продуктов, необходимых для приготовления выбранных блюд.

Целевая аудитория проекта - люди, увлеченные кулинарией, желающие готовить много и вкусно, а также обмениваться своим кулинарным опытом.

Рабочий сайт: [https://foodgram.sytes.net](https://foodgram.sytes.net)

---

## Стек технологий
- **Backend**: Python, Django, Django ORM, Django REST Framework, Djoser
- **Frontend**: React
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker
- **CI/CD**: GitHub Actions
- **Веб-сервер**: Nginx
- **WSGI-сервер**: Gunicorn

---

## CI/CD Пайплайн
Проект автоматизирован с использованием GitHub Actions. Вот основные этапы пайплайна:

1. **Тестирование кода**:
   - Проверка кода на соответствие стандартам с помощью `flake8`.
   
2. **Сборка и публикация Docker-образов**:
   - Собираются и публикуются образы для:
     - Backend (`foodgram_backend`)
     - Frontend (`foodgram_frontend`)
     - Gateway (Nginx) (`foodgram_gateway`)

3. **Деплой на удаленный сервер**:
   - Обновление Docker Compose на удаленном сервере.
   - Применение миграций, сбор статики и перезапуск контейнеров.

4. **Уведомление о завершении деплоя**:
   - Отправка сообщения в Telegram о успешном завершении деплоя.

Полный конфигурационный файл `.github/workflows/main.yml` можно найти в репозитории.

---

## Локальное развертывание с Docker

### Клонирование репозитория
```bash
git clone https://github.com/Beaver-IK/foodgram.git
cd foodgram
```
### Переход в папку с docker-compose.yml
```bash
cd infra
```
### Создание файла .env
```env
# Настройки базы данных
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_HOST=db
DB_PORT=5432

# Конфигурация Django
ENV=dev  # или prod
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGIN_WHITELIST=http://localhost:3000
```

### Запуск контейнеров
```bash
docker-compose up -d
```

### Применение миграций и сбор статики
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```

### Создание суперпользователя
```bash
docker compose exec -it backend bash
python manage.py createsuperuser
```

### Использование docker-compose.develop.yml (опционально)
Если вы хотите собирать образы локально вместо загрузки их с Docker Hub,
используйте файл docker-compose.develop.yml:
```bash
docker-compose -f docker-compose.develop.yml up -d
```

### Тома Docker
- **foodgram_pg_data** : Том для базы данных PostgreSQL.
- **foodgram_static** : Том для статических файлов.
- **foodgram_media** : Том для медиафайлов.

### Версии инструментов
Все версии инструментов указаны в файлах:

- ***/requirements/***: зависимости Python
- ***/frontend/package.json***: зависимости Node.js для фронтенда.