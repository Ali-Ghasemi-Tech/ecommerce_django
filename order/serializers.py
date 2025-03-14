from rest_framework import serializers
from .models import Order, Payment, OrderItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'created_at', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
fields = ['user', 'total_price', 'status', 'items']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'payment_date', 'amount', 'payment_method', 'status']

class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
