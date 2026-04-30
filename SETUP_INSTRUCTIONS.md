# 🚀 Retail System — Setup Instructions

Backend-сервис автоматизации закупок на стеке **Django + DRF + PostgreSQL + Redis + Celery**.

Документ описывает полный процесс запуска проекта и полностью соответствует текущей реализации API.

---

# 📦 1. Клонирование проекта

```bash
git clone https://github.com/Sleeping-Beauty-G/diploma_project.git
cd diploma_project
```

---

# 🐳 2. Запуск через Docker (рекомендуется)

Проект полностью контейнеризирован.

## 🔧 Сборка и запуск

```bash
docker compose up --build
```

или в фоне:

```bash
docker compose up -d --build
```

---

## 📌 Проверка контейнеров

```bash
docker compose ps
```

Ожидаемые сервисы:

| Service | Status       |
| ------- | ------------ |
| web     | ✔ Running    |
| db      | ✔ PostgreSQL |
| redis   | ✔ Running    |
| celery  | ✔ Running    |

---

## 🌐 Доступ к API

```
http://localhost:8000/api/
```

Админка:

```
http://localhost:8000/admin/
```

---

# 🗄 3. Миграции базы данных

```bash
docker compose exec web python manage.py migrate
```

---

# 👤 4. Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

# 🔐 5. Аутентификация (JWT)

## Получение токена

```http
POST /api/token/
```

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

## Использование

```
Authorization: Bearer <access_token>
```

---

# 📡 6. Основные API endpoints

## 👤 Пользователи

| Endpoint       | Описание    |
| -------------- | ----------- |
| /api/register/ | Регистрация |

---

## 🏠 Адреса

| Endpoint             | Описание              |
| -------------------- | --------------------- |
| /api/addresses/      | Список / создание     |
| /api/addresses/{id}/ | Обновление / удаление |

---

## 📦 Товары

| Endpoint            | Описание       |
| ------------------- | -------------- |
| /api/products/      | Список товаров |
| /api/products/{id}/ | Детали         |

---

## 📊 Предложения поставщиков

| Endpoint                | Описание           |
| ----------------------- | ------------------ |
| /api/product-info/      | Список предложений |
| /api/product-info/{id}/ | Детали             |

---

## 🛒 Корзина (CartItem)

| Endpoint                     | Описание            |
| ---------------------------- | ------------------- |
| /api/cart/items/             | Получить корзину    |
| POST /api/cart/items/        | Добавить товар      |
| PATCH /api/cart/items/{id}/  | Изменить количество |
| DELETE /api/cart/items/{id}/ | Удалить товар       |

---

## 📑 Заказы

| Endpoint                        | Описание          |
| ------------------------------- | ----------------- |
| /api/orders/                    | Список заказов    |
| /api/orders/{id}/               | Детали            |
| /api/orders/checkout/           | Оформление заказа |
| /api/orders/{id}/change_status/ | Изменение статуса |

---

# 📥 7. Импорт товаров

## Через Celery

```python
from products.tasks import import_products
import_products.delay("data/shop_data.yaml")
```

## Через management команду

```bash
docker compose exec web python manage.py import_products
```

---

# ⚡ 8. Celery и фоновые задачи

Используется для:

* отправки email после заказа
* фоновой обработки

## Проверка

```bash
docker compose logs celery
```

Ожидаемый вывод:

```
Connected to redis://...
```

⚠️ Для отправки email необходимо указать реальные SMTP данные.

---

# ⚙️ 9. Переменные окружения

Создайте `.env` файл:

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

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

---

# 🔐 10. Роли пользователей

| Роль     | Возможности         |
| -------- | ------------------- |
| client   | корзина, заказы     |
| supplier | управление товарами |
| admin    | полный доступ       |

---

# 🧪 11. Проверка работоспособности

```bash
curl -H "Authorization: Bearer <token>" \
http://localhost:8000/api/products/
```

---

# 🛑 12. Остановка проекта

```bash
docker compose down
```

---

# 🧾 13. Полная пересборка

```bash
docker compose down -v
docker compose up --build
```

---

# ⚠️ 14. Возможные проблемы

## Контейнеры не запускаются

```bash
docker compose logs
```

---

## База данных не готова

```bash
docker compose restart db
```

---

## Celery не работает

```bash
docker compose restart celery
```

---

## Порт занят

Измените в `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"
```

---

# 🏁 Итог

После запуска доступны:

✔ REST API (Django DRF)
✔ PostgreSQL база
✔ Redis брокер
✔ Celery задачи
✔ Импорт товаров
✔ Система заказов
✔ JWT-аутентификация

---

# 💬 Примечание

Рекомендуется использовать Docker для запуска, чтобы обеспечить стабильную и воспроизводимую среду.

Проект готов к демонстрации и защите дипломной работы.
