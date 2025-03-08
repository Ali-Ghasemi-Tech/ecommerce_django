from django.urls import path, include
from .views import CartAPIView, AddToCartAPIView, RemoveFromCartAPIView, OrderAPIView, PaymentAPIView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'cart', CartApiView, basename="cart")

urlpatterns = [
    path('cart/', CartAPIView.as_view({'get': 'list'}), name='api_cart'),
    path('cart/add/<int:product_id>/', AddToCartAPIView.as_view(), name='api_add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', RemoveFromCartAPIView.as_view(), name='api_remove_from_cart'),
    path('order/<int:order_id>/', OrderAPIView.as_view(), name='api_order'),
    path('payment/<int:order_id>/', PaymentAPIView.as_view(), name='api_payment'),
    # path('', include(router.urls)),
]