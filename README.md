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

Добавьте в настройках setting.py
```
INSTALLED_APPS = [
    'lenivastore.apps.LenivastoreConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'paypal.standard.ipn',
    'payment.apps.PaymentConfig',
    'cupons.apps.CuponsConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'phonenumber_field',
]
```

В TEMPLATES > context_processors
```
'cart.context_processors.cart',
'lenivastore.context_processors.categories_base',
```

Так же в settings
```
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CART_SESSION_ID = 'cart'
```

Настройки отправки сообщений

Для вывода в консоль
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Или для реальной отправки писем
```
EMAIL_BACKEND = your_emil_backend
EMAIL_HOST = your_email_host
EMAIL_PORT = your_email_port
EMAIL_HOST_USER = your_email_host_user
EMAIL_HOST_PASSWORD = your_email_host_password
EMAIL_USE_TLS = your_email_use_tls (True/False)
EMAIL_USE_SSL = your_email_use_ssl (True/False)
DEFAULT_FROM_EMAIL = your_email_host_user

```

Настройки paypal
```
PAYPAL_RECEIVER_EMAIL = your_email_host_user
PAYPAL_TEST = (True/False)
```

> Не забудьте настроить свою базу данных

Добавьте в ваш urls.py
```
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('lenivastore.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('order/', include('orders.urls', namespace='orders')),
    path('cupons/', include('cupons.urls', namespace='cupon')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

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