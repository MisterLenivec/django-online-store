from django.urls import include, path

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('page_ordered_goods/', views.page_ordered_goods,
         name='page_ordered_goods'),
    path('change_phone_or_image/', views.change_phone_or_image,
         name='change_phone_or_image'),
]
