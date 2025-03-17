from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    

    class Meta:
        model = OrderItem
        fields = ['product', 'access_expiry_date']
    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = ['customer', 'date','total_price', 'items']

    
    def get_total_price(self, obj):
        return obj.calculate_total_price()
