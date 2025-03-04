from django.urls import path , include
from .views import CartApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/cart' , CartApiView , basename="cart")
urlpatterns = [
    path('', include(router.urls)),
]
