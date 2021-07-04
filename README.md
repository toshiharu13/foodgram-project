# Продуктовый помощник

![Foodgram](https://github.com/toshiharu13/foodgram-project/actions/workflows/main.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

[Сайт доступен по ссылке.](http:///)

## Техническое описание
___
**Инфраструктура**

Проект использует базу данных [PostgrSQL](https://www.postgresql.org/).

В корневой папке расположен файл requirements.txt со всеми зависимостями.

Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) через docker-compose на сервере в [Yandex.Cloud](https://cloud.yandex.ru/).
## Системные требования
______


- [Python 3](https://www.python.org/)
- [Django 3.0.5](https://www.djangoproject.com/)
- [REST API Framework](https://www.django-rest-framework.org/)
- [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [NGINX](https://www.nginx.com/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [PostgrSQL](https://www.postgresql.org/)
- [Yandex.Cloud](https://cloud.yandex.ru/)


##  Установка
______

Для устновки проекта пребуется:
- [Python 3](https://www.python.org/)
- [PostgrSQL](https://www.postgresql.org/)
- [venv](https://docs.python.org/3/library/venv.html)
- [GitHub](https://github.com/git-guides/install-git)

После выполнения push необходимо зайти на сервер

    $ ssh <nickname>@<IP адрес>

Перейти в директорию app

    $ cd app/

Выполнить миграции

    $ docker-compose exec web python manage.py migrate

Выгрузить данные из файла csv

    $ docker-compose exec web python manage.py import_csv

Собрать статику
    
    $ docker-compose exec web python manage.py collectstatic --noinput
    
Загрузить тестовую базу

    $ docker-compose exec web python manage.py loaddata dump.json