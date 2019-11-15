from django.urls import include, path

from . import views


app_name = 'lenivastore'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('/<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about_project, name='about_project'),
]
