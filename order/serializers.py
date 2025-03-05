from rest_framework import serializers
<<<<<<< HEAD
from .models import Cart, Order, Payment, CartItem, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'items']
=======
from .models import Order, OrderItem , Cart , CartItem
>>>>>>> 252e1006c79bb694332783572f85d3eb81a31da8

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
<<<<<<< HEAD
        fields = ['user', 'total_price', 'status', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'payment_date', 'amount', 'payment_method', 'status']


=======
        fields = '__all__'  # تمامی فیلدها

class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
>>>>>>> 252e1006c79bb694332783572f85d3eb81a31da8
