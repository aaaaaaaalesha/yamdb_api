<h1 align="center"> Командный проект YaMDb </h1>

<p align="center">
  <a href="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  </a>
  <a href="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
    <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
  </a>
  <a href="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
    <img alt="DjangoREST" src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
  </a>
  <a href="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens">
    <img alt="JWT" src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens">
  </a>
  <a href="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
    <img alt="SQLite" src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
  </a>

REST API проекта сбора отзывов и оценок пользователей на произведения.
</p> 

## Установка

Как развернуть наш проект у себя.

1. Склонируйте репозиторий

```
$ git clone https://github.com/aaaaaaaalesha/api_yamdb.git
$ cd api_yamdb
```

2. Создайте и активируйте рекламное окружение

```
$ python3 -m venv venv
$ venv/bin/activate
```

3. Установите зависимости

```
$ pip install -r requirements.txt
```

4. Выполните миграции

```
$ cd api_yamdb
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ cd ..
```

4. Запуск сервера

```
$ python3 .\api_yamdb\manage.py runserver
```

5. Импортирование тестовых данных из CSV в базу данных

```
$ cd api_yamdb
$ python3 manage.py import_database [path, ...]
```
, где `path` - путь до директории с csv-файлами или до самих файлов по отдельности, параметр опциональный, по умолчанию
файлы будут взяты из директории `/api_yamdb/static/data`.

## Примеры

Некоторые примеры запросов к API. 
Более подробную информацию можно посмотреть при запуске проекта на странице Redoc, например: http://127.0.0.1:8000/redoc/

### 1. Регистрация нового пользователя

Получить код подтверждения на переданный `email`. Права доступа: Доступно без токена. Использовать имя 'me' в качестве `username` запрещено. Поля `email` и username должны быть уникальными.

`[POST] /api/v1/auth/signup/`

```json
{
  "email": "bla2132143@yandex.ru",
  "username": "login123"
}
```

- `Status Code: 200`

```json
{
  "email": "bla2132143@yandex.ru",
  "username": "login123"
}
```
При этом пользователю приходит письмо следующего содержания:

```
From: yamdb@yandex.ru
To: bla2132143@yandex.ru
Date: Wed, 08 Feb 2023 17:48:42 -0000
Message-ID: <167587852265.2372.2942627407382418585@PC>

Привет, login123!
Нам пришёл запрос на регистрацию от Вас. Если это были не Вы, игнорируйте это письмо!
Ваш код подтверждения: OCMH5
Для окончания регистрации Вам необходимо выполнить запрос:
[POST] /auth/token/
{
  "username": "login123",
  "confirmation_code": "OCMH5"
}
```

### 2. Получение JWT-токена

Получение JWT-токена в обмен на username и confirmation code. Права доступа: Доступно без токена.

`[POST] /api/v1/auth/token/`

```json
{
  "username": "login123",
  "confirmation_code": "OCMH5"
}
```

- `Status Code: 200`

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4Mjk4MDk4LCJpYXQiOjE2NzU4Nzg4OTgsImp0aSI6ImFhOWY1ZjZlMmE2MzQzMGE5MjhkMWI1Yjg0NTNmYWFhIiwidXNlcl9pZCI6MX0.ipOVw6wvRs57COYm8J0ozm-HzHrcX9Rqm6taxr74Xe4"
}
```

### 3. Добавление новой категории

Создать категорию. Права доступа: Администратор. Поле slug каждой категории должно быть уникальным.

`[POST] /api/v1/categories/`

```json
{
  "name": "Фильм",
  "slug": "film"
}
```

- `Status Code: 201`

```json
{
  "name": "Фильм",
  "slug": "film"
}
```

### 3. Добавление нового жанра

Добавить жанр. Права доступа: Администратор. Поле slug каждого жанра должно быть уникальным.

`[POST] /api/v1/genres/`

```json
{
  "name": "Боевик",
  "slug": "action"
}
```

- `Status Code: 201`

```json
{
  "name": "Боевик",
  "slug": "action"
}
```

## Авторы

|              Автор             |                       Контакт                      |
|:------------------------------:|:--------------------------------------------------:|
| Алексей Александров (teamlead) | [@aaaaaaaalesha](https://github.com/aaaaaaaalesha) |
|         Ольга Панарина         | [@OlgaPanarina](https://github.com/OlgaPanarina)   |
|        Максим Ласточкин        | [@Mificus](https://github.com/Mificus)             |