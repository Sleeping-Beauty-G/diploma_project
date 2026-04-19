# 📦 Retail System API Documentation
## 🧾 Общее описание

**Backend-приложение для автоматизации закупок в розничной сети.**
**Реализовано на Django + Django REST Framework + Celery + PostgreSQL + Redis.**

**Система поддерживает:**

- управление товарами и поставщиками
- корзину пользователя
- оформление заказов
- асинхронные задачи (email, импорт)
- JWT-аутентификацию
---
## 🌐 Базовый URL
```
http://localhost:8000/api/
```
---
## 🔐 1. Аутентификация
**Регистрация**

POST ```/api/register/```

**Request:**
```json
{
  "username": "user1",
  "email": "user@mail.com",
  "password": "strongpassword",
  "role": "client"
}
```
**Response:**
```json
{
  "id": 1,
  "username": "user1",
  "email": "user@mail.com",
  "role": "client"
}
```
### Получение JWT токена

POST``` /api/token/```

**Request:**
```json
{
  "username": "user1",
  "password": "strongpassword"
}
```
**Response:**
```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```
---
## 🔑 Использование токена

Во всех защищённых запросах:
```
Authorization: Bearer <access_token>
```
---
## 📦 2. Товары
### Получение списка товаров

GET ```/api/products/```

**Response:**
```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "description": "Smartphone",
    "product_infos": [
      {
        "id": 1,
        "supplier": "Apple Supplier",
        "price": 1200.00,
        "quantity": 10,
        "parameters": [
          {
            "parameter": {
              "name": "Color"
            },
            "value": "Black"
          }
        ]
      }
    ]
  }
]
```
---
## 📊 Предложения товаров

GET ```/api/productinfo/``` (если подключишь роутер)
---

## 🛒 3. Корзина
### Получить корзину

GET ```/api/cart/```

**Response:**
```json
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
```
---
### Добавить товар

POST ```/api/cart/add/```
```json
{
  "product_id": 1,
  "quantity": 2
}
```
---
### Удалить товар

POST ```/api/cart/remove/```
```json
{
  "product_id": 1
}
```
---
## 📦 4. Заказы
### Создание заказа (Checkout)

POST ```/api/orders/confirm/```

**Request:**
```json
{
  "address": "Amsterdam, Main Street 1"
}
```
**Response:**
```json
{
  "status": "order confirmed",
  "order_id": 1
}
```
---
### Получение списка заказов

GET ```/api/orders/```

**Response:**
```json
[
  {
    "id": 1,
    "address": "Amsterdam, Main Street 1",
    "created_at": "2026-04-19T10:00:00Z",
    "status": "confirmed",
    "items": [
      {
        "product": 1,
        "supplier": 1,
        "quantity": 2,
        "price": 1200.00
      }
    ]
  }
]
```
---
## Изменение статуса заказа

POST ```/api/orders/{id}/change_status/```

```json
{
  "status": "shipped"
}
```
---
## 📌 Возможные статусы заказа
- new — новый
- confirmed — подтверждён
- paid — оплачен
- shipped — отправлен
- delivered — доставлен
- canceled — отменён
---
## 📥 5. Импорт товаров
### Через Celery
```python
from products.tasks import import_products
import_products.delay("shop_data.yaml")
```
---

### Через management command
```
docker compose exec web python manage.py import_products
```
---

## 📄 Формат YAML
```YAML
products:
  - name: iPhone 15
    supplier: Apple
    price: 1200
    stock: 10
    parameters:
      Color: Black
      Memory: 128GB
```
---
## ⚙️ 6. Асинхронные задачи

Используется:

- **Celery** — выполнение задач
- **Redis** — брокер
**Пример задачи:**
- отправка email после оформления заказа
---
## 👥 7. Роли пользователей
- client — покупатель
- supplier — поставщик
- admin — администратор
## ❗ 8. Ошибки API
| Код | Описание        |
| --- | --------------- |
| 400 | Неверный запрос |
| 401 | Не авторизован  |
| 403 | Нет доступа     |
| 404 | Не найдено      |
| 500 | Ошибка сервера  |

## 🧪 9. Пример использования (cURL)
**Получить товары**
```
curl http://localhost:8000/api/products/
```
**Добавить в корзину**
```
curl -X POST http://localhost:8000/api/cart/add/ \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"product_id": 1, "quantity": 2}'
```
# 🏁 Итог

## API поддерживает:

- ✔ JWT авторизацию
- ✔ управление товарами
- ✔ корзину
- ✔ оформление заказов
- ✔ асинхронные задачи
- ✔ импорт данных