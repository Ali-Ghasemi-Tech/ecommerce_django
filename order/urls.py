from django.urls import path
<<<<<<< HEAD
from .views import AddToOrderView , OrderListView

urlpatterns = [
    path('add-to-order/', AddToOrderView.as_view(), name='add-to-order'),
    path('orders/', OrderListView.as_view(), name='order-list')
=======
from .views import  OrderDetailView, OrderItemDeleteView
from .views import request_payment, verify_payment

urlpatterns = [
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('item/<int:order_item_id>/delete/', OrderItemDeleteView.as_view(), name='order-item-delete'),
    # path('pay/', request_payment, name='request_payment'),
    # path('verify/', verify_payment, name='verify_payment'),
>>>>>>> my-new-branch
]