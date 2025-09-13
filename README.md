# **Pleo**

<p align="center">
  <img src="https://img.shields.io/badge/platform-%20WEB-blue?style=for-the-badge" alt="WEB">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/fastapi-0.116.1-darkgreen?style=for-the-badge" alt="FastAPI">
  <a href="https://github.com/cloudsucker/pleo/commits/main/">
    <img src="https://img.shields.io/badge/status-done-brightgreen?style=for-the-badge" alt="Status">
  </a>
  <a href="https://github.com/cloudsucker/pleo/issues">
    <img src="https://img.shields.io/github/issues/cloudsucker/pleo?style=for-the-badge&logo=github" alt="Issues">
  </a>
</p>

---

**Pleo** — это минималистичная социальная сеть реализованная на FastAPI с поддержкой регистрации, авторизации, публикации постов, профилей пользователей и ленты (`The Wall`).

![logo](static/logo.png)

Проект был создан в учебных целях и демонстрирует архитектуру современного Python веб-приложения.

![post](static/screenshots/post-1.png)

---

### **Регистрация и авторизация**

<p align="center">
  <figure style="display:inline-block; margin: 0 16px;">
    <img src="static/screenshots/register.png" alt="Register page" height="320">
    <figcaption align="center">Регистрация</figcaption>
  </figure>
  <figure style="display:inline-block; margin: 0 16px;">
    <img src="static/screenshots/login.png" alt="Login page" height="320">
    <figcaption align="center">Авторизация</figcaption>
  </figure>
</p>

### **Лента постов (The Wall)**

![the_wall](static/screenshots/the_wall.png)

_Страница с постами пользователей с поддержкой `Markdown`._

### **Profile Settings**

![profile_settings](static/screenshots/profile_settings.png)

_Страница настроек аккаунта (смена аватарки, username и пароля)._

## **🧭 Содержание**

-   [📦 Установка](#-установка)
-   [🧪 Тестирование](#-тестирование)
-   [🧱 Архитектура проекта](#-архитектура-проекта)
-   [✅ ROADMAP](#-roadmap)
-   [🔗 Зависимости](#-зависимости)
-   [📬 Обратная связь](#-обратная-связь)

## **📦 Установка**

**Клонируйте репозиторий:**

```bash
git clone https://github.com/cloudsucker/pleo.git
cd pleo
```

### **Docker Compose:**

```bash
docker compose up --build
```

### **Без Docker:**

#### **1. Создайте виртуальное окружение:**

```bash
python -m venv .venv
```

#### **2. Активируйте виртуальное окружение:**

-   **Windows**:

        ```bash
        .venv\Scripts\activate
        ```

-   **Linux/MacOS**:

        ```bash
        source .venv/bin/activate
        ```

#### 3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

#### 4. **Запуск:**

Запустите файл `main.py` из папки `app`:

```bash
cd app
uvicorn main:app --reload
```

> ![IMPORTANT]
> Обратите внимание, что запуск без Docker осуществляется из директории `/app`.

## **🧪 Тестирование**

В проекте не реализованы отдельные тесты, но вы можете проверить работу API вручную через `Postman` или `curl`, либо добавить свои тесты с помощью `unittest`/`pytest`.

**Буду рад помощи тестировщиков :)**

## **🧱 Архитектура проекта**

```
pleo/
├── app/
│   ├── main.py         # Точка входа FastAPI
│   ├── db.py           # Подключение к БД и сессии
│   ├── models/         # SQLAlchemy-модели (User, Post, Session)
│   ├── routers/        # FastAPI-роутеры (user, post, auth, wall, profile)
│   ├── schemas/        # Pydantic-схемы (DTO, валидация)
│   ├── static/         # Статика, шаблоны, стили, html
│   └── ...
├── requirements.txt    # Зависимости
├── dockerfile          # Docker-образ приложения
├── compose.yml         # Docker Compose (FastAPI + Postgres)
└── README.md
```

-   FastAPI backend с роутерами для пользователей, постов, профиля, стены и авторизации
-   SQLAlchemy ORM, PostgreSQL (docker)
-   Jinja2 для шаблонов страниц
-   Авторизация через сессии (cookie)
-   Вся логика — в папке `app/`

## **✅ ROADMAP**

-   [x] Базовая регистрация и авторизация
-   [x] CRUD для пользователей и постов
-   [x] Лента постов (стена)
-   [x] Профиль пользователя
-   [x] Docker-окружение (FastAPI + Postgres)
-   [ ] Администраторы
    -   [ ] Создание тикетов в тех-поддержку
    -   [ ] Модерация постов
    -   [ ] Сброс пароля через админов
-   [ ] Главная страница
-   [ ] Тесты и CI
-   [ ] Улучшение UI/UX
-   [ ] Поддержка комментариев и лайков
-   [ ] Документация OpenAPI/Swagger

## 🔗 **Зависимости**

-   fastapi[standard]
-   jinja2
-   passlib
-   sqlalchemy
-   psycopg2-binary
-   markdown2

## 📬 **Обратная связь**

**Репозиторий активно развивается, буду рад обратной связи.**

**По всем вопросам:** ferjenkill@gmail.com
