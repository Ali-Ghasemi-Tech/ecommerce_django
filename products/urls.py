from django.urls import path
from .views import ProductListApi, ProductDetailApi

urlpatterns = [
    path('', ProductListApi.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailApi.as_view(), name='product-detail'),
]