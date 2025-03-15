from rest_framework import serializers
from .models import OrderItem , Order
from products.serializers import ProductDetailSerializer 
from account.models import Account

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)  

    class Meta:
        model = OrderItem
        fields = ['product', 'access_expiry_date']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  
    #customer = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())  # فیلد customer

    class Meta:
        model = Order
        fields = ['customer', 'date', 'status', 'total_price', 'items']


