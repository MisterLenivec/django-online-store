from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views


app_name = 'lenivastore'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('/<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.product_detail, name='product_detail')
]
