from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'  # تمامی فیلدها

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # نمایش آیتم‌های سفارش

    class Meta:
        model = Order
        fields = '__all__'  # تمامی فیلدها
