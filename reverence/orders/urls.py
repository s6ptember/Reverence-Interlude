from django.urls import path
from .views import order_create, order_success


app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('completed/', order_success, name='order_success'),
]
