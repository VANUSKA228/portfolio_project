# DEVfolio 

Платформа для создания портфолио разработчиков с автоматической подгрузкой проектов из GitHub.

## 🚀 Функциональность (MVP, в разработке)

- Регистрация и вход по логину/паролю
- Две роли: обычный пользователь и администратор
- Переключатель тёмной/светлой темы (сохраняется в браузере)
- Режим impersonation (техподдержка) для администратора
- Главная страница с поиском пользователей по ID или имени
- Профиль пользователя с гибкой настройкой портфолио:
  - Три пресета отображения: сетка, Bento Grid, витрина
  - Привязка репозиториев GitHub (OAuth)
  - Автоматическая подгрузка README.md и ссылок на демо (GitHub Pages)
- Администратор может заходить в аккаунты пользователей (impersonation)

## 🧱 Стек технологий

| Компонент        | Технология                                |
|------------------|-------------------------------------------|
| Бэкенд           | Python 3.11, Django 6.0.5                 |
| Фронтенд         | Чистый CSS (кастомные свойства, темы), Vanilla JS |
| База данных      | SQLite                                    |
| Аутентификация   | Django Auth, GitHub OAuth (django-allauth)|
| Контроль версий  | Git, GitHub                               |

## 📦 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/твой_username/portfolio_project.git
cd portfolio_project
```

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Выполнить миграции

```bash
python manage.py migrate
```

### 5. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер разработки

```bash
python manage.py runserver
```

### 7. Открыть в браузере

```text
http://127.0.0.1:8000/
```

## 📁 Структура проекта

```text
portfolio_project/
├── config/                # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              # Приложение пользователей
│   ├── models.py          # Кастомная модель User (роль)
│   ├── views.py           # Регистрация, выход
│   ├── urls.py
│   ├── forms.py           # Форма регистрации
│   └── admin.py
├── core/                  # Основное приложение
│   ├── views.py           # Главная, профиль
│   └── urls.py
├── static/
│   └── css/
│       └── style.css      # Кастомные стили (тёмная/светлая тема)
├── templates/             # HTML-шаблоны
│   ├── base.html
│   ├── home.html
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   ├── user_profile.html
│   └── admin_profile.html
├── manage.py
├── requirements.txt
└── README.md
```

## 📋 Статус проекта

Находится на этапе MVP. Реализован каркас:

- Регистрация
- Роли пользователей
- Главная страница
- Профили пользователей

## 🔮 Планируется

- Личная информация пользователя (фото, описание)
- Интеграция с GitHub OAuth
- Пресеты портфолио
- Поиск пользователей
- Панель администратора
