# 🚀 Retail System — Setup Instructions

Backend-сервис автоматизации закупок на стеке **Django + DRF + PostgreSQL + Redis + Celery**.

Документ описывает полный процесс запуска проекта в локальной среде.

---

# 📦 1. Клонирование проекта

Склонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone <your-repository-url>
cd retail_system
```

---

# 🐳 2. Запуск через Docker (рекомендуется)

Проект полностью контейнеризирован и готов к запуску через Docker.

## 🔧 Сборка и запуск

```bash
docker compose up --build
```

или в фоновом режиме:

```bash
docker compose up -d --build
```

---

## 📌 Проверка контейнеров

```bash
docker compose ps
```

Ожидаемые сервисы:

| Service | Status                 |
| ------- | ---------------------- |
| web     | ✔ Running              |
| db      | ✔ Running (PostgreSQL) |
| redis   | ✔ Running              |
| celery  | ✔ Running              |

---

## 🌐 Доступ к API

После запуска:

```
http://localhost:8000/api/
```

---

# 🗄 3. Миграции базы данных

Обычно выполняются автоматически при старте контейнера.

При необходимости вручную:

```bash
docker compose exec web python manage.py migrate
```

---

# 👤 4. Создание суперпользователя (опционально)

Для доступа к Django Admin:

```bash
docker compose exec web python manage.py createsuperuser
```

Админка будет доступна по адресу:

```
http://localhost:8000/admin/
```

---

# 📥 5. Импорт товаров

Проект поддерживает импорт товаров из YAML-файла.

## 🔹 Вариант 1: через Celery (рекомендуется)

```python
from products.tasks import import_products
import_products.delay("shop_data.yaml")
```

## 🔹 Вариант 2: через Django команду

```bash
docker compose exec web python manage.py import_products
```

---

# 📧 6. Celery и асинхронные задачи

Система использует:

* **Celery** — обработка фоновых задач
* **Redis** — брокер сообщений

## 🔍 Проверка Celery

```bash
docker compose logs celery
```

Если всё работает корректно, вы увидите:

```
[INFO/MainProcess] Connected to redis://...
```

---

# 🧠 7. Архитектура сервисов

| Service | Описание                 |
| ------- | ------------------------ |
| web     | Django REST API          |
| db      | PostgreSQL база данных   |
| redis   | Брокер сообщений         |
| celery  | Worker для фоновых задач |

---

# ⚙ 8. Переменные окружения

Файл `.env`:

```env
SECRET_KEY=supersecretkey123
DEBUG=True

POSTGRES_DB=retail_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

---

# 🔐 9. Аутентификация (JWT)

Проект использует JWT-аутентификацию.

## Получение токена

```http
POST /api/token/
```

Пример запроса:

```json
{
  "username": "user",
  "password": "password"
}
```

## Обновление токена

```http
POST /api/token/refresh/
```

---

# 📦 10. Основные API endpoints

| Endpoint                | Описание          |
| ----------------------- | ----------------- |
| `/api/register/`        | Регистрация       |
| `/api/token/`           | Получение JWT     |
| `/api/products/`        | Каталог товаров   |
| `/api/cart/`            | Корзина           |
| `/api/orders/checkout/` | Оформление заказа |

---

# 🧪 11. Проверка работоспособности

## 🔹 Проверка API

```bash
curl http://localhost:8000/api/products/
```

## 🔹 Проверка контейнеров

```bash
docker compose ps
```

---

# 🛑 12. Остановка проекта

```bash
docker compose down
```

---

# 🧾 13. Полная пересборка (если возникли ошибки)

```bash
docker compose down -v
docker compose up --build
```

---

# ⚠️ 14. Возможные проблемы и решения

### ❌ Контейнер не запускается

```bash
docker compose logs
```

---

### ❌ База данных не готова

Решение: подождать или перезапустить

```bash
docker compose restart db
```

---

### ❌ Celery не обрабатывает задачи

```bash
docker compose restart celery
```

---

### ❌ Порт 8000 занят

Измените порт в `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

---

# 🏁 Итог

После успешного запуска система включает:

✔ Django REST API
✔ PostgreSQL базу данных
✔ Redis брокер
✔ Celery фоновые задачи
✔ Импорт товаров
✔ Систему заказов
✔ JWT-аутентификацию

---

# 💬 Примечание

Проект полностью готов к разработке, тестированию и демонстрации на защите диплома.

Рекомендуется запуск через Docker для максимальной воспроизводимости среды.




