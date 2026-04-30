# 📦 Retail System API Documentation

Полноценный backend-сервис для автоматизации закупок в розничной сети.
API реализован на Django REST Framework с поддержкой аутентификации, ролей пользователей и асинхронных задач.

---

# 🔐 Аутентификация

API использует JWT-аутентификацию.

Все защищённые запросы требуют заголовок:

```
Authorization: Bearer <your_token>
```

---

# 👤 Регистрация

### POST `/api/register/`

Создание нового пользователя.

#### Request:

```json
{
  "username": "user1",
  "email": "user@example.com",
  "password": "strongpassword",
  "role": "client"
}
```

#### Response:

```json
{
  "id": 1,
  "username": "user1",
  "email": "user@example.com",
  "role": "client"
}
```

---

# 🏠 Адреса доставки

## GET `/api/addresses/`

Получить список адресов пользователя

## POST `/api/addresses/`

Создать новый адрес

```json
{
  "city": "Paris",
  "street": "Main Street",
  "house": "10A"
}
```

## PATCH `/api/addresses/{id}/`

Обновить адрес

## DELETE `/api/addresses/{id}/`

Удалить адрес

---

# 🛍️ Товары

## GET `/api/products/`

Получить список товаров

## GET `/api/products/{id}/`

Получить информацию о товаре

---

# 📦 Предложения поставщиков

## GET `/api/product-info/`

Список предложений (цены, остатки)

## GET `/api/product-info/{id}/`

Детальная информация

---

# 🛒 Корзина

Работа с корзиной реализована через ресурс **CartItem**.

## GET `/api/cart/items/`

Получить содержимое корзины

## POST `/api/cart/items/`

Добавить товар в корзину

```json
{
  "product": 1,
  "quantity": 2
}
```

## PATCH `/api/cart/items/{id}/`

Изменить количество товара

```json
{
  "quantity": 5
}
```

## DELETE `/api/cart/items/{id}/`

Удалить товар из корзины

---

# 📦 Заказы

## GET `/api/orders/`

Получить список заказов пользователя

## GET `/api/orders/{id}/`

Получить детали заказа

---

## 🧾 Оформление заказа

### POST `/api/orders/checkout/`

Создаёт заказ на основе корзины.

```json
{
  "address": "Paris, Main Street 10A"
}
```

#### Response:

```json
{
  "status": "order created",
  "order_id": 1
}
```

---

## 🔄 Изменение статуса заказа

### PATCH `/api/orders/{id}/change_status/`

```json
{
  "status": "paid"
}
```

### Доступные статусы:

* `new`
* `confirmed`
* `paid`
* `shipped`
* `delivered`
* `canceled`

---

# 🔐 Роли пользователей

Система поддерживает роли:

| Роль     | Возможности         |
| -------- | ------------------- |
| client   | корзина, заказы     |
| supplier | управление товарами |
| admin    | полный доступ       |

---

# ⚙️ Асинхронные задачи

После оформления заказа запускается Celery-задача:

* отправка email-уведомления

---

# ❗ Обработка ошибок

Пример ошибки:

```json
{
  "error": "Cart is empty"
}
```

Коды ответов:

* `200` — OK
* `201` — Created
* `400` — Bad Request
* `401` — Unauthorized
* `404` — Not Found

---

# 🧠 Особенности реализации

* Используются транзакции (`transaction.atomic`)
* Защита от race condition (`select_for_update`)
* REST-архитектура (ресурс CartItem)
* Разграничение доступа через permissions
* Асинхронная обработка через Celery

---

# 🚀 Быстрый старт

```bash
git clone <repo>
cd project

docker compose up --build
```

---
