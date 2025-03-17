from django.urls import path
from .views import  OrderDetailView, OrderItemDeleteView

urlpatterns = [
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('item/<int:order_item_id>/delete/', OrderItemDeleteView.as_view(), name='order-item-delete'),
]