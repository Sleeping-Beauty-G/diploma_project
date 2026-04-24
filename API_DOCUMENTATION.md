# 📦 Retail System API Documentation

## 🧾 Общее описание

Backend-приложение для автоматизации закупок и управления заказами в розничной сети.

### Используемый стек
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery

### Основные возможности
- JWT-аутентификация
- Управление товарами и поставщиками
- Корзина пользователя (CRUD)
- Оформление и управление заказами
- Асинхронные задачи
- Импорт товаров из YAML

---

## 🌐 Базовый URL

http://localhost:8000/api/

---

## 🔐 Аутентификация

### Регистрация пользователя

POST /api/register/

Request:
{
  "username": "user1",
  "email": "user@mail.com",
  "password": "strongpassword",
  "role": "client"
}

Response:
{
  "id": 1,
  "username": "user1",
  "email": "user@mail.com",
  "role": "client"
}

---

### Получение JWT токена

POST /api/token/

Request:
{
  "username": "user1",
  "password": "strongpassword"
}

Response:
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}

---

### Использование токена

Authorization: Bearer <access_token>

---

## 📦 Товары

### Получить список товаров

GET /api/products/

### Получить предложения поставщиков

GET /api/productinfo/

---

## 🛒 Корзина

### Получить корзину

GET /api/cart/

Response:
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": 1,
      "quantity": 2
    }
  ]
}

### Добавить товар в корзину

POST /api/cart/items/

{
  "product_id": 1,
  "quantity": 2
}

### Изменить количество товара

PATCH /api/cart/items/{id}/

{
  "quantity": 5
}

### Удалить товар из корзины

DELETE /api/cart/items/{id}/

---

## 📦 Заказы

### Создать заказ

POST /api/orders/

{
  "address": "Amsterdam, Main Street 1"
}

Response:
{
  "id": 1,
  "status": "confirmed"
}

### Получить список заказов

GET /api/orders/

### Получить заказ по ID

GET /api/orders/{id}/

### Изменить статус заказа

PATCH /api/orders/{id}/status/

{
  "status": "shipped"
}

---

## 📌 Возможные статусы заказа

- new
- confirmed
- paid
- shipped
- delivered
- canceled

---

## 📥 Импорт товаров

### Через Celery

from products.tasks import import_products
import_products.delay("shop_data.yaml")

### Через management command

docker compose exec web python manage.py import_products

---

## 📄 Формат YAML

products:
  - name: iPhone 15
    supplier: Apple
    price: 1200
    stock: 10
    parameters:
      Color: Black
      Memory: 128GB

---

## ⚙️ Асинхронные задачи

Используются:
- Celery
- Redis

Примеры:
- отправка email после оформления заказа
- импорт товаров в фоне

---

## 👥 Роли пользователей

- client — покупатель
- supplier — поставщик
- admin — администратор

### Разграничение доступа

- Клиент управляет своей корзиной и заказами
- Поставщик управляет своими товарами
- Администратор имеет полный доступ

---

## ❗ Ошибки API

| Код | Описание |
|------|----------|
| 400 | Неверный запрос |
| 401 | Не авторизован |
| 403 | Нет доступа |
| 404 | Не найдено |
| 500 | Внутренняя ошибка сервера |

---

## 🧪 Примеры использования

### Получить товары

curl http://localhost:8000/api/products/

### Добавить товар в корзину

curl -X POST http://localhost:8000/api/cart/items/ 
-H "Authorization: Bearer <token>" 
-H "Content-Type: application/json" 
-d '{"product_id": 1, "quantity": 2}'

---

## 🏁 Итог

API поддерживает:

- JWT-аутентификацию
- Управление товарами
- Управление корзиной
- Оформление и отслеживание заказов
- Асинхронные задачи
- Импорт данных
- Разграничение прав доступа