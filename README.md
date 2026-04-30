# 🛒 Retail System API

🚀 **Retail System API** — backend-сервис для автоматизации закупок и управления заказами в розничной сети.
Проект реализован на **Django + Django REST Framework** с использованием асинхронных задач (**Celery + Redis**) и контейнеризации (**Docker**).

---

## ✨ Основной функционал

* 👤 Регистрация пользователей и роли (client / supplier / admin)
* 🔐 JWT-аутентификация (SimpleJWT)
* 📦 Каталог товаров и предложений поставщиков
* 🛒 Управление корзиной (RESTful API)
* 📑 Оформление и управление заказами
* 📉 Контроль и списание остатков
* ⚡ Асинхронные задачи (Celery)
* 📧 Email-уведомления
* 📥 Импорт товаров из YAML
* 🐳 Полная Docker-инфраструктура

---

## 🏗 Архитектура

* **Django REST Framework** — API
* **PostgreSQL** — база данных
* **Redis** — брокер сообщений
* **Celery** — фоновые задачи
* **Docker / Docker Compose** — запуск и деплой

---

## 📦 Структура проекта

```
retail_system/
│
├── orders/        # корзина и заказы
├── products/      # товары, параметры, импорт
├── suppliers/     # поставщики
├── users/         # пользователи, роли, адреса
├── retail_system/ # настройки Django
```

---

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/Sleeping-Beauty-G/diploma_project.git
cd diploma_project
```

### 2. Запуск проекта

```bash
docker compose up --build
```

### 3. Миграции

```bash
docker compose exec web python manage.py migrate
```

### 4. Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🌐 API

**Базовый URL:**

```
http://localhost:8000/api/
```

---

## 🔐 Аутентификация

### Получение токена

```
POST /api/token/
```

```json
{
  "username": "user",
  "password": "password"
}
```

### Обновление токена

```
POST /api/token/refresh/
```

### Использование

```
Authorization: Bearer <access_token>
```

---

## 📡 Основные endpoints

### 👤 Пользователи

* `POST /api/register/` — регистрация

---

### 🏠 Адреса

* `GET /api/addresses/` — список адресов
* `POST /api/addresses/` — создать
* `PATCH /api/addresses/{id}/` — обновить
* `DELETE /api/addresses/{id}/` — удалить

---

### 📦 Товары

* `GET /api/products/` — список товаров
* `GET /api/products/{id}/` — детали

---

### 📊 Предложения поставщиков

* `GET /api/product-info/` — список предложений
* `GET /api/product-info/{id}/` — детали

---

### 🛒 Корзина (CartItem — REST ресурс)

* `GET /api/cart/items/` — получить корзину
* `POST /api/cart/items/` — добавить товар

```json
{
  "product": 1,
  "quantity": 2
}
```

* `PATCH /api/cart/items/{id}/` — изменить количество

```json
{
  "quantity": 5
}
```

* `DELETE /api/cart/items/{id}/` — удалить товар

---

### 📑 Заказы

* `GET /api/orders/` — список заказов
* `GET /api/orders/{id}/` — детали

---

### 🧾 Оформление заказа

```
POST /api/orders/checkout/
```

```json
{
  "address": "Paris, Main Street 10A"
}
```

---

### 🔄 Изменение статуса

```
PATCH /api/orders/{id}/change_status/
```

```json
{
  "status": "paid"
}
```

---

### 📌 Доступные статусы

* `new`
* `confirmed`
* `paid`
* `shipped`
* `delivered`
* `canceled`

---

## 📥 Импорт товаров

```bash
docker compose exec web python manage.py import_products
```

---

## ⚡ Celery

Используется для:

* отправки email после заказа
* фоновой обработки задач

Запуск:

```bash
docker compose up celery
```

---

## 🐳 Docker сервисы

| Service | Description |
| ------- | ----------- |
| web     | Django API  |
| db      | PostgreSQL  |
| redis   | Broker      |
| celery  | Worker      |

---

## ⚙️ Переменные окружения

Создай `.env` файл:

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

## 🧠 Особенности реализации

* ✔ RESTful архитектура (ресурс CartItem)
* ✔ Разграничение доступа по ролям
* ✔ Транзакции (`transaction.atomic`)
* ✔ Защита от race condition (`select_for_update`)
* ✔ Асинхронные задачи (Celery)
* ✔ Масштабируемая структура проекта

---

## 🧪 Проверка

```bash
curl -H "Authorization: Bearer <token>" \
http://localhost:8000/api/products/
```

---

## 🛑 Остановка

```bash
docker compose down
```

---

## 📌 Статус проекта

* ✅ Готов к проверке
* 🎓 Дипломный проект
* 🚀 Архитектура приближена к production

---

## 👩‍💻 Автор

Гюнай Меджидова
https://github.com/Sleeping-Beauty-G

---

## 📚 Дополнительная документация

* 📖 **API_DOCUMENTATION.md** — подробное описание API
* 🚀 **SETUP_INSTRUCTIONS.md** — инструкция по запуску
* 🛠 **FIXES_REPORT.md** — отчёт по доработкам

---

💡 Проект демонстрирует разработку REST API с применением современных инструментов backend-разработки и готов к дальнейшему расширению.
