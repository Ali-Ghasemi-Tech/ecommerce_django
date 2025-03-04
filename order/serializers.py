from rest_framework import serializers
from .models import Order, OrderItem , Cart , CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'  # تمامی فیلدها

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # نمایش آیتم‌های سفارش

    class Meta:
        model = Order
        fields = '__all__'  # تمامی فیلدها

class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
