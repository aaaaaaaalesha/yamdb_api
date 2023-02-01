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

## Примеры

Некоторые примеры запросов к API.

... `TODO`

## Авторы

|              Автор             |                       Контакт                      |
|:------------------------------:|:--------------------------------------------------:|
| Алексей Александров (teamlead) | [@aaaaaaaalesha](https://github.com/aaaaaaaalesha) |
|         Ольга Панарина         | [@OlgaPanarina](https://github.com/OlgaPanarina)   |
|        Максим Ласточкин        | [@Mificus](https://github.com/Mificus)             |