# django-online-store
Интернет-магазин на Django
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/MisterLenivec/django-online-store/blob/master/LICENSE)

### Технологии:
- Django 2.2
- Python 3.7
- HTML, CSS (Flexbox, Grid)
- Javascript
- Postgresql

Проект является интеренет-магазином, предоставляющим товары.

Через админ панель можно добавлять и удалять товары и категории, а так же 
описание к ним, просматривать и отмечать заказы, добавлять и удалять купоны на 
скидки, просматривать пользователей и их профили.
Пользователи могут выбирать товары, добавлять в корзину, применять купоны на 
скидки, оформлять заказ. После заказа присылается сообщение по электронной 
почте, с деталями заказа, а так же PDF файл. Реализованна регистрация и 
авторизация, профиль пользователя с возможностью просмотра заказов и изменением 
аватара пользователя.


Быстрый старт
--
```
$ git clone https://github.com/MisterLenivec/django-online-store.git
$ cd django-online-store
$ pip install -r requirements.txt
```

> Не забудьте настроить свою базу данных

Миграции и создание супер пользователя
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> Используйте адрес: http://127.0.0.1:8000/

По желанию можете добавить в папку media дефолтную картинку для пользователя 
(default.jpg).

Пример https://lenivastore.herokuapp.com/
