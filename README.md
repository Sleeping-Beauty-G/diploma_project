# 📦 Retail System API

Backend-сервис для автоматизации закупок в розничной сети.

Проект реализует полноценную e-commerce backend систему:

- каталог товаров от поставщиков  
- корзину покупателя  
- оформление заказов  
- систему статусов заказа  
- импорт товаров из YAML  
- асинхронные задачи (Celery + Redis)  
- email-уведомления  
- JWT-аутентификацию  

---

## 🧱 Tech Stack

- Python 3.11  
- Django 5.2  
- Django REST Framework  
- PostgreSQL  
- Redis  
- Celery  
- Docker / Docker Compose  

---

## 📁 Architecture

- `users/` — пользователи и регистрация (JWT, роли)  
- `products/` — товары, прайс-листы, импорт YAML  
- `suppliers/` — поставщики  
- `orders/` — корзина, заказы, бизнес-логика  
- `retail_system/` — настройки Django + Celery + URLs  

📄 `shop_data.yaml` — файл импорта товаров  

---

## 🚀 Quick Start

### 1. Клонировать проект
```bash
git clone <repo-url>
cd retail_system
```
## 🚀 Setup & Run

### 2. Создать `.env` файл

```env id="env123"
SECRET_KEY=supersecretkey123
DEBUG=True

POSTGRES_DB=retail_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```
### 3. Запуск проекта
```bash
docker compose up --build
```
### 4. Миграции
```bash
docker compose exec web python manage.py migrate
```
### 5. Создание суперпользователя
```bash
docker compose exec web python manage.py createsuperuser
```
## 🌐 Base URL
```bash
http://localhost:8000/api/
```
## 🔐 Authentication
Регистрация
```bash
POST /api/register/
```
```json
{
  "username": "user1",
  "email": "user@mail.com",
  "password": "123456",
  "role": "client"
}
```
### JWT Token
```htpp
POST /api/token/
POST /api/token/refresh/
```
### 📦 Products API
**Получить список товаров**
```htpp
GET /api/products/
```
**Получить товар**
```htpp
GET /api/products/{id}/
```
### 🧺 Cart API
**Добавить товар**
```htpp
POST /api/cart/add/
```
```json
{
  "product_id": 1,
  "quantity": 2
}
```
**Получить корзину**
```htpp
GET /api/cart/
```
**Удалить товар**
```htpp
POST /api/cart/remove/
```
### 📦 Orders API
**Оформить заказ**
```htpp
POST /api/orders/confirm/
```
```json
{
  "address": "Moscow, Lenina 10"
}
```
### Получить мои заказы
```htpp
GET /api/orders/
```
Изменение статуса заказа (admin/supplier)

```
POST /api/orders/{id}/change_status/
```

```json
{
  "status": "shipped"
}
```
## 📊 Order Status System
- NEW — новый заказ
- CONFIRMED — подтверждён
- PAID — оплачен
- SHIPPED — отправлен
- DELIVERED — доставлен
- CANCELED — отменён
## 📥 Import System (YAML)
**Через Django command**
```bash
docker compose exec web python manage.py import_products
```

**Через Celery**
```python
import_products.delay("shop_data.yaml")
```
## ⚙️ Celery Tasks

Асинхронные процессы:

- отправка email после заказа
- импорт товаров из YAML
## 📧 Email Notifications

Отправляется автоматически:

- после оформления заказа
- через Celery worker (асинхронно)

## 🐳 Docker Services
| Service | Description    |
| ------- | -------------- |
| web     | Django API     |
| db      | PostgreSQL     |
| redis   | message broker |
| celery  | async tasks    |

Запуск
```
docker compose up --build
```
Остановка
```
docker compose down
```
## 🔁 Business Logic
- один пользователь = одна корзина
- корзина → источник заказа
- цена фиксируется при оформлении
- товары могут быть от разных поставщиков
- списание склада происходит при создании заказа
- все операции защищены transaction.atomic()
## 🔥 Key Features
- ✔ JWT авторизация
- ✔ REST API
- ✔ Cart system
- ✔ Order lifecycle
- ✔ Supplier system
- ✔ YAML import
- ✔ Celery async tasks
- ✔ Email notifications
- ✔ Docker setup
- ✔ PostgreSQL + Redis
## 🧪 Testing

### Рекомендуется:

- Postman
- Insomnia
curl
## 🎓 Diploma Coverage

### Проект соответствует требованиям:

- ✔ Django ORM
- ✔ DRF API
- ✔ PostgreSQL
- ✔ Redis
- ✔ Celery
- ✔ Docker
- ✔ Асинхронные задачи
- ✔ Импорт данных
- ✔ Email уведомления
- ✔ Бизнес-логика интернет-магазина
## 🏁 Conclusion

Проект представляет собой полноценную backend-систему уровня **production-ready MVP** для автоматизации закупок и управления заказами.

## 👩‍💻 Автор Студент:
Гюнай Меджидова(https://github.com/Sleeping-Beauty-G)

Дипломный проект:
**Retail System API**
--- 
## 📚 Дополнительная документация

**В проекте представлена подробная техническая документация:**

* 📖 API документация — API_DOCUMENTATION.md
Полное описание всех endpoints, структуры запросов и ответов, примеры использования.
* 🚀 Инструкция по запуску — SETUP_INSTRUCTIONS.md
Пошаговое руководство по развертыванию проекта через Docker и локально.
* 🛠 Отчёт по исправлениям — FIXES_REPORT.md
Список внесённых улучшений, исправленных ошибок и оптимизаций проекта.
---
