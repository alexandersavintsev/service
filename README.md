## FastAPI-сервис для получения топ-N постов по лайкам

### 📌 Описание проекта

Этот проект представляет собой API-сервис на базе **FastAPI**, обрабатывающий HTTP-запросы и возвращающий топ N постов по количеству лайков. Проект разработан в рамках финального задания курса от [karpov.courses](https://karpov.courses/ml-start?_gl=1*1p6bprb*_ga*MTUyNTQzNDkxMi4xNzUwNDEzNDQ1*_ga_DZP7KEXCQQ*czE3NTA0MTM0NDQkbzEkZzEkdDE3NTA0MTQ0MTMkajU3JGwwJGgw).

---

### 🛠️ Стек технологий

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic

---

### 📂 Структура проекта

```bash
.
├── app.py            # Основная точка запуска FastAPI-приложения с эндпоинтами
├── database.py       # Подключение к базе данных
├── main.py           # Вспомогательный файл для проверки
├── schema.py         # Pydantic-схемы для сериализации
├── table_post.py     # ORM-модель таблицы post и SQL-запрос через select
├── table_user.py     # ORM-модель таблицы user + группировка по (country, os)
├── table_feed.py     # ORM-модель таблицы feed_action + связи
```

---

### 📝 Этапы разработки и содержание файлов

#### 🔸Предварительно создаем файл  `database.py`

- Установлено подключение к базе данных через SQLAlchemy
- Создан движок с указанием URL PostgreSQL
- Настроен `SessionLocal` — сессия для взаимодействия с БД
- Создан Base — основа для всех ORM-моделей

#### 🔸Создаем файл  `table_post.py`

- Создан класс `Post` на базе SQLAlchemy (добавлена ORM-модель `Post`)
- Реализован SQL-запрос для выборки 10 последних постов с темой `"business"`.

#### 🔸Создаем файл `table_user.py`

- Реализована модель `User` на SQLAlchemy (добавлена ORM-модель `User`)
- Выполнен групповой запрос по (`country, os`) с фильтром `group = 3`
- Отбор пар с количеством записей `> 100`
- Результат выводится списком кортежей

#### 🔸Создаем файл  `table_feed.py`

- Модель `Feed`, соответствующая таблице `feed_action`
- Поля `user_id` и `post_id` определены с использованием `ForeignKey`
- Используется `Base` из `database.py`
- Связи через `relationship()` пока не реализованы

#### 🔸Создаем файл  `schema.py`

- Содержит Pydantic-модели `UserGet, PostGet и FeedGet`
- Каждая модель отражает структуру соответствующей таблицы в БД
- Все поля строго типизированы
- Установлено `orm_mode = True` для корректной сериализации ORM-объектов

#### 🔸Создаем файл  `app.py`

- Инициализировано FastAPI-приложение
- Эндпоинты:
  - `/user/{id}` — получить одного пользователя
  - `/post/{id}` — получить один пост
  - `/user/{id}/feed?limit=N` — действия пользователя (по умолчанию 10)
  - `/post/{id}/feed?limit=N` — действия по посту (по умолчанию 10)
- Для feed-эндпоинтов реализована сортировка по убыванию времени
- Обработка ошибок: 404 при отсутствии сущностей, 200 с пустым списком при отсутствии действий

#### 🔸Создаем связи между  `table_feed.py` и `schema.py` 

- В `Feed` добавлены поля `user` и `post` — `relationship()` к таблицам `User` и `Post`
- В `FeedGet` (Pydantic) добавлены поля `user: UserGet` и `post: PostGet`
- FastAPI теперь возвращает вложенные структуры с полными данными, а не только id
- Валидация вложенных объектов осуществляется через Pydantic автоматически

#### 🔸Добавляем endpoint /post/recommendations/ в  `app.py`

- GET /post/recommendations/ с query-параметрами:
  - `id` — пока не используется
  - `limit` — количество возвращаемых постов (по умолчанию 10)
- Подсчёт количества лайков (`action='like'`) по таблице feed
- Сортировка по убыванию количества лайков
- Возврат списка объектов PostGet (id, text, topic)

---

### 🚀 Как запустить проект

1. Клонируйте репозиторий
```bash
git clone https://github.com/alexandersavintsev/service.git
cd service
```

2. Установите зависимости
```bash
pip install -r requirements.txt
```

Если файла `requirements.txt` ещё нет — создайте его с такими строками:
```bash
fastapi==0.75.1
pandas==1.4.2
sqlalchemy==1.4.35
requests==2.27.1
catboost==1.0.6
numpy==1.22.4
pydantic==1.9.1
scikit_learn==1.1.1
lightgbm==3.3.2
xgboost==1.6.1
psycopg2-binary==2.9.3
uvicorn==0.16.0
category-encoders==2.5.0
loguru==0.6.0
implicit==0.5.2
lightfm==1.16
tqdm==4.62.0
matplotlib==3.4.2
nltk==3.8.1
pyarrow==5.0.0
scipy==1.7.1
seaborn==0.11.1
statsmodels==0.12.2
```

3. Запуск сервера
```bash
uvicorn app:app --reload
```

---

### 📎 Пример запроса

🔹 Получить топ-5 постов по лайкам:
```bash
GET /post/recommendations/?limit=5
```

Пример вывода:
```bash
[
  {
    "id": 123,
    "text": "Очень интересный пост",
    "topic": "tech"
  },
  ...
]
```

---

### 👨‍💻 Автор
Проект выполнен в рамках курса [karpov.courses](https://karpov.courses/ml-start?_gl=1*1p6bprb*_ga*MTUyNTQzNDkxMi4xNzUwNDEzNDQ1*_ga_DZP7KEXCQQ*czE3NTA0MTM0NDQkbzEkZzEkdDE3NTA0MTQ0MTMkajU3JGwwJGgw).

Автор: alexandersavintsev

GitHub: https://github.com/alexandersavintsev/service

---

MIT License
Copyright (c) 2025 alexandersavintsev
