from django.urls import path
from .views import ProductListApi, ProductDetailApi , CommentListCreateView

urlpatterns = [
    path('', ProductListApi.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailApi.as_view(), name='product-detail'),
    path('<int:product_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]