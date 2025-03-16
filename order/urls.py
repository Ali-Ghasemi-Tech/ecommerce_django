from django.urls import path
from .views import OrderCreateView, OrderDetailView, OrderItemDeleteView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('item/<int:order_item_id>/delete/', OrderItemDeleteView.as_view(), name='order-item-delete'),
]