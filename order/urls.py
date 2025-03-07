from django.urls import path, include
from .views import CartAPIView, AddToCartAPIView, RemoveFromCartAPIView, OrderAPIView, PaymentAPIView, CartApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/cart', CartApiView, basename="cart")

urlpatterns = [
    path('api/cart/', CartAPIView.as_view(), name='api_cart'),
    path('api/cart/add/<int:product_id>/', AddToCartAPIView.as_view(), name='api_add_to_cart'),
    path('api/cart/remove/<int:cart_item_id>/', RemoveFromCartAPIView.as_view(), name='api_remove_from_cart'),
    path('api/order/<int:order_id>/', OrderAPIView.as_view(), name='api_order'),
    path('api/payment/<int:order_id>/', PaymentAPIView.as_view(), name='api_payment'),
    path('', include(router.urls)),
]