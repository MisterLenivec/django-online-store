from django.urls import path
from .views import cupon_apply


app_name = 'cupons'

urlpatterns = [
    path('apply/', cupon_apply, name='apply')
]
