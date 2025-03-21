from django.urls import path
from .views import AddToOrderView , OrderListView

urlpatterns = [
    path('add-to-order/', AddToOrderView.as_view(), name='add-to-order'),
    path('orders/', OrderListView.as_view(), name='order-list')
]