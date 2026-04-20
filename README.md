# 🛒 Retail System API

🚀 **Retail System API** — backend-сервис для автоматизации закупок и управления заказами в розничной сети.

Проект реализован на **Django + Django REST Framework** с поддержкой асинхронных задач (Celery), контейнеризацией (Docker) и PostgreSQL в качестве основной базы данных.

---

## ✨ Основной функционал

- 👤 Регистрация и управление пользователями
- 🔐 JWT-аутентификация (SimpleJWT)
- 📦 Каталог товаров и поставщиков
- 🛒 Корзина покупателя
- 📑 Оформление заказов
- 📉 Списание остатков со склада
- ⚡ Асинхронная обработка задач (Celery + Redis)
- 📧 Email-уведомления о заказах
- 📥 Импорт товаров из YAML файла
- 🐳 Полная контейнеризация через Docker

---

## 🏗 Архитектура проекта

- **Django REST Framework** — REST API
- **PostgreSQL** — база данных
- **Redis** — брокер сообщений
- **Celery** — асинхронные задачи
- **Docker / Docker Compose** — развёртывание

---

## 📦 Структура проекта
```
retail_system/
│
├── orders/ # Корзина, заказы
├── products/ # Товары, импорт, параметры
├── suppliers/ # Поставщики
├── users/ # Пользователи и регистрация
├── retail_system/ # Настройки Django
```
 ---

## 🚀 Быстрый старт

### 1. Клонирование проекта

```bash
git clone https://github.com/Sleeping-Beauty-G/diploma_project.git
cd diploma_project
```
---

### 2. Запуск через Docker
```
docker compose up --build
```
---
### 3. Применение миграций
```
docker compose exec web python manage.py migrate
```
---
### 4. Создание суперпользователя
```
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
Получение токена
```htpp
POST/api/token/
```
```json
{
  "username": "user",
  "password": "password"
}
```
### Использование токена
```
Authorization: Bearer <access_token>
```
---
### 📡 Основные endpoints
**👤 Пользователи**
- POST /api/register/ — регистрация
**📦Товары**
- GET /api/products/ — список товаров
**🛒 Корзина**
- POST /api/cart/add/ — добавить товар
- POST /api/cart/remove/ — удалить товар
**📑 Заказы**
- POST /api/orders/confirm/ — оформить заказ
- GET /api/orders/ — список заказов
---
## 📥 Импорт товаров

Импорт через YAML:
```bash
docker compose exec web python manage.py import_products
```
---
## ⚡ Celery задачи

Celery используется для:

- отправки email после заказа
- фоновой обработки задач

Запуск воркера:
```bash
docker compose up celery
```
## 🐳 Docker сервисы

| Service | Description |
| ------- | ----------- |
| web     | Django API  |
| db      | PostgreSQL  |
| redis   | Broker      |
| celery  | Worker      |

---
## ⚙️ Переменные окружения

Создай .env файл:
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
## 🧠 Особенности проекта
- ✔ Асинхронная обработка заказов
- ✔ Контроль остатков на складе
- ✔ Docker-ready архитектура
- ✔ Расширяемая модульная структура
- ✔ RESTful API дизайн
---
## 🧪 Проверка работы
```bash
curl http://localhost:8000/api/products/
```
---
## 🛑 Остановка проекта
```bash
docker compose down
```
---
### 📌 Статус проекта

- ✅ Готов к использованию
- 📚 Учебный / дипломный проект
- 🚀 Может быть расширен до production уровня
---

## 👩‍💻 Автор Студент:
Гюнай Меджидова(https://github.com/Sleeping-Beauty-G)

Проект выполнен в рамках дипломной работы по backend-разработке.



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
