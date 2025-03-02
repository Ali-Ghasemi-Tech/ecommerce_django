from django.urls import path
from .views import create_order

urlpatterns = [
    path('create-order/', create_order, name='create_order'),
    # path('orders/', order_list, name='order_list'),

]
