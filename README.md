# 🛒 Retail System API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-4.x-green.svg)
![DRF](https://img.shields.io/badge/DRF-REST%20API-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgres-DB-blue.svg)
![Celery](https://img.shields.io/badge/celery-async_tasks-yellow.svg)
![Docker](https://img.shields.io/badge/docker-containerized-blue.svg)
![JWT](https://img.shields.io/badge/auth-JWT-orange.svg)

---

## 🚀 Описание проекта

**Retail System API** — backend-сервис для автоматизации закупок и управления заказами в розничной сети.

Проект реализован на **Django + Django REST Framework** с применением современных backend-подходов:

* REST архитектура
* JWT-аутентификация (SimpleJWT)
* Ролевая модель доступа (RBAC)
* Асинхронные задачи (Celery + Redis)
* Контейнеризация (Docker / Docker Compose)
* Транзакционная безопасность (atomic + select_for_update)

---

## ✨ Основной функционал

* 👤 Регистрация пользователей (client / supplier / admin)
* 🔐 JWT-аутентификация
* 📦 Каталог товаров (Product)
* 📊 Предложения поставщиков (ProductInfo)
* 🛒 Корзина как REST ресурс (CartItem)
* 📑 Оформление заказов (checkout)
* 📉 Контроль и списание остатков
* 📧 Email-уведомления (Celery)
* 📥 Импорт товаров из YAML
* ⚡ Асинхронные задачи (Celery)
* 🐳 Docker инфраструктура

---

## 🏗 Архитектура проекта

* Django REST Framework — API слой
* PostgreSQL — база данных
* Redis — брокер сообщений
* Celery — фоновые задачи
* Docker / Docker Compose — инфраструктура

---

## 📦 Структура проекта

```text
retail_system/
├── users/
├── products/
├── suppliers/
├── orders/
├── retail_system/
```

---

## 🚀 Быстрый старт

```bash
git clone <repo-url>
cd retail_system
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 🌐 Base URL

```
http://localhost:8000/api/
```

---

## 🔐 Authentication

```
POST /api/token/
POST /api/token/refresh/
```

---

## 👤 Registration

```
POST /api/register/
```

---

## 📡 API Endpoints

### 📦 Products

* GET `/api/products/`
* GET `/api/products/{id}/`

---

### 📊 Product Info

* GET `/api/product-info/`
* GET `/api/product-info/{id}/`
* POST `/api/product-info/import_yaml/`

📌 Доступ:

* admin / supplier (ограниченный доступ)

---

### 🛒 Cart (REST Resource)

* GET `/api/cart/items/`
* POST `/api/cart/items/`
* PATCH `/api/cart/items/{id}/`
* DELETE `/api/cart/items/{id}/`

---

### 📑 Orders

* GET `/api/orders/`
* GET `/api/orders/{id}/`
* POST `/api/orders/checkout/`

---

### 🔄 Order Status

```
PATCH /api/orders/{id}/change_status/
```

📌 Доступ:

* admin
* supplier

---

## 🏠 Addresses API

📌 Только для авторизованных пользователей

* GET `/api/addresses/`
* POST `/api/addresses/`
* PATCH `/api/addresses/{id}/`
* DELETE `/api/addresses/{id}/`

---

## 📥 YAML Import

```
POST /api/product-info/import_yaml/
```

📌 Выполняется асинхронно через Celery

---

## ⚡ Celery Tasks

Используется для:

* отправки email при регистрации
* отправки email при оформлении заказа
* импорта YAML файлов

---

## 🔐 Permissions (важно для проверки)

| Endpoint                  | Role             |
| ------------------------- | ---------------- |
| /cart                     | client           |
| /orders                   | client           |
| /addresses                | client           |
| /product-info/import_yaml | supplier / admin |
| /orders/change_status     | admin / supplier |

---

## 🧠 Ключевые архитектурные решения

* RESTful архитектура (CartItem как ресурс)
* Разделение логики (Service Layer подход)
* Асинхронные задачи (Celery)
* Защита от race condition (select_for_update)
* Транзакционная безопасность (atomic)
* RBAC (role-based access control)

---

## 📘 Swagger / ReDoc

### Swagger UI

```
http://localhost:8000/swagger/
```

### ReDoc

```
http://localhost:8000/redoc/
```

📌 Swagger генерируется автоматически из DRF схемы и полностью соответствует реальному API.

---

## ⚠️ Error Response

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 📊 HTTP Status Codes

| Code | Meaning      |
| ---- | ------------ |
| 200  | OK           |
| 201  | Created      |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 403  | Forbidden    |
| 404  | Not Found    |

---

## 🐳 Docker Services

| Service | Description   |
| ------- | ------------- |
| web     | Django API    |
| db      | PostgreSQL    |
| redis   | Celery broker |
| celery  | worker        |

---

## 🚀 Project Status

✔ REST API полностью реализован
✔ JWT Authentication
✔ Cart / Orders / Products
✔ YAML import + Celery
✔ RBAC система
✔ Swagger документация
✔ Готов к защите

---

## 👩‍💻 Author

Гюнай Меджидова
GitHub: https://github.com/Sleeping-Beauty-G

---

💡 Проект демонстрирует разработку production-style REST API с использованием Django REST Framework, Celery, PostgreSQL, Redis и Docker.
