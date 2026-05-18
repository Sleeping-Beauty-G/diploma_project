# 📦 Retail System API Documentation

REST API для автоматизации закупок и управления заказами в розничной сети.

Проект реализован на **Django REST Framework** с использованием:

* JWT (SimpleJWT)
* PostgreSQL
* Redis
* Celery
* Docker / Docker Compose

---

# 🌐 Base URL

```
http://localhost:8000/api/
```

---

# 🔐 Authentication

API использует JWT-аутентификацию.

Для доступа к защищённым endpoint необходимо передавать токен:

```
Authorization: Bearer <access_token>
```

---

# 🔑 Auth Endpoints

## POST `/api/token/`

### Request

```json
{
  "username": "admin",
  "password": "password"
}
```

### Response

```json
{
  "refresh": "jwt_refresh_token",
  "access": "jwt_access_token"
}
```

---

## POST `/api/token/refresh/`

Обновление access token.

---

# 👤 Registration

## POST `/api/register/`

Регистрация пользователя + отправка welcome email (Celery task).

### Request

```json
{
  "username": "user1",
  "email": "user@example.com",
  "password": "StrongPass123",
  "role": "client"
}
```

### Response

```json
{
  "id": 1,
  "username": "user1",
  "email": "user@example.com",
  "role": "client"
}
```

---

# 🏠 Address API

📌 Только для авторизованных пользователей

## GET `/api/addresses/`

Список адресов текущего пользователя.

## POST `/api/addresses/`

Создание адреса.

### Request

```json
{
  "city": "Paris",
  "street": "Main Street",
  "house": "10A"
}
```

## PATCH `/api/addresses/{id}/`

Обновление адреса.

## DELETE `/api/addresses/{id}/`

Удаление адреса.

---

# 📦 Products API

## GET `/api/products/`

Список товаров (read-only)

## GET `/api/products/{id}/`

Детали товара

---

# 📊 Product Info API

## GET `/api/product-info/`

## GET `/api/product-info/{id}/`

📌 Доступ:

* supplier (только свои товары)
* admin (все товары)

---

# 📥 Import YAML (Celery)

## POST `/api/product-info/import_yaml/`

📌 Доступ:

* supplier
* admin

### Request

```json
{
  "file_path": "shop_data.yaml"
}
```

### Response

```json
{
  "status": "import started"
}
```

---

# 🛒 Cart API (CartItem REST resource)

## GET `/api/cart/items/`

## POST `/api/cart/items/`

## PATCH `/api/cart/items/{id}/`

## DELETE `/api/cart/items/{id}/`

### Add item

```json
{
  "product": 1,
  "quantity": 2
}
```

---

# 📑 Orders API

## GET `/api/orders/`

Список заказов пользователя

## GET `/api/orders/{id}/`

Детали заказа

---

# 🧾 Checkout

## POST `/api/orders/checkout/`

Создание заказа из корзины.

### Request

```json
{
  "address": "Paris, Main Street 10A"
}
```

### Response

```json
{
  "status": "order created",
  "order_id": 1
}
```

---

# 🔄 Order Status

## PATCH `/api/orders/{id}/change_status/`

📌 Доступ:

* admin
* supplier

### Request

```json
{
  "status": "paid"
}
```

### Allowed statuses:

* new
* confirmed
* paid
* shipped
* delivered
* canceled

---

# ⚠️ Permissions Model

| Role     | Access level               |
| -------- | -------------------------- |
| client   | cart, orders, addresses    |
| supplier | product info (own), import |
| admin    | full access                |

---

# 📧 Celery Tasks

Используется для:

* отправки email при регистрации
* отправки email после оформления заказа
* импорт YAML файлов

---

# ❗ Error Response

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

# 📊 HTTP Status Codes

| Code | Meaning      |
| ---- | ------------ |
| 200  | OK           |
| 201  | Created      |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 403  | Forbidden    |
| 404  | Not Found    |

---

# 🐳 Docker Services

| Service | Description   |
| ------- | ------------- |
| web     | Django API    |
| db      | PostgreSQL    |
| redis   | Celery broker |
| celery  | worker        |

---

# 📘 Swagger / ReDoc

## Swagger UI

```
http://localhost:8000/swagger/
```

## ReDoc

```
http://localhost:8000/redoc/
```

📌 Используется для:

* тестирования API
* проверки endpoints
* демонстрации преподавателю

---

# 🧠 Technical Stack

* Django REST Framework
* JWT Authentication
* Celery + Redis
* PostgreSQL
* Docker
* Role-based permissions
* Transactions (`atomic`)
* ORM optimization (`select_related`, `prefetch_related`)

---

# 🚀 Project Status

* ✅ Fully working REST API
* ✅ JWT auth
* ✅ Cart / Orders / Products
* ✅ Celery tasks
* ✅ Swagger docs
* ✅ Role-based access control
* ✅ Ready for final defense
