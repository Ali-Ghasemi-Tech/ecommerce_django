
from django.urls import path
from . import views

urlpatterns = [
    path('home/' , views.home , name='home'),
    path('<int:pk>/' , views.product_detail , name='product_detail'),
    path('category/<int:pk>/' , views.category_view , name='category_view'),
    path('cart/' , views.cart_view , name='cart_view'),
    path('add_to_cart/<int:pk>/' , views.add_to_cart , name='add_to_cart'),
    path('remove_from_cart/<int:pk>/' , views.remove_from_cart , name='remove_from_cart'),
    path('order/<int:pk>/' , views.order_view , name='order_view'),
    path('payment/<int:pk>/' , views.payment_view , name='payment_view'),
    path('review/<int:pk>/' , views.review_view , name='review_view'),
    path('search/<int:pk>/' , views.search_view , name='search_review'),
   
        
]