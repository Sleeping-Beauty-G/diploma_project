# 🚀 Retail System API — Setup Instructions

Полная инструкция по запуску backend-сервиса **Retail System API**.

Проект реализован на **Django + Django REST Framework** с использованием Docker, PostgreSQL и Celery.

---

## 📦 Требования

Перед запуском убедитесь, что установлено:

* Docker
* Docker Compose
* Git

---

## 📥 Клонирование проекта

```bash
git clone https://github.com/Sleeping-Beauty-G/diploma_project.git
cd diploma_project
```

---

## ⚙️ Настройка окружения

Создайте `.env` файл в корне проекта:

```env
SECRET_KEY=your_secret_key
DEBUG=True

POSTGRES_DB=retail_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## 🐳 Запуск проекта (Docker)

### 1. Сборка и запуск контейнеров

```bash
docker compose up --build
```

---

### 2. Выполнить миграции

```bash
docker compose exec web python manage.py migrate
```

---

### 3. Создать суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🌐 Доступ к проекту

После запуска сервис доступен:

* API: http://localhost:8000/api/
* Swagger: http://localhost:8000/swagger/
* ReDoc: http://localhost:8000/redoc/
* Admin panel: http://localhost:8000/admin/

---

## 📥 Импорт данных

Импорт товаров из YAML:

```bash
docker compose exec web python manage.py import_products
```

---

## ⚡ Celery (фоновые задачи)

Запуск Celery worker:

```bash
docker compose up celery redis
```

---

## 🔐 Авторизация

### Получение токена

`POST /api/token/`

```json
{
  "username": "admin1",
  "password": "AdminPass123"
}
```

### Response

```json
{
  "refresh": "token",
  "access": "token"
}
```

---

## 🧪 Проверка работы API

```bash
curl -H "Authorization: Bearer <token>" \
http://localhost:8000/api/products/
```

---

## 🐛 Возможные проблемы

### 1. Контейнеры не запускаются

```bash
docker system prune -a
```

### 2. Ошибка миграций

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 3. Celery не работает

* проверь Redis контейнер
* проверь CELERY_BROKER_URL в `.env`

---

## 📌 Итог

После выполнения всех шагов проект полностью готов к запуску и проверке.

---

## 🚀 Статус проекта

* ✅ Dockerized
* ✅ Django REST API
* ✅ Celery async tasks
* ✅ JWT authentication
* ✅ Swagger documentation
* 🎓 Ready for defense
