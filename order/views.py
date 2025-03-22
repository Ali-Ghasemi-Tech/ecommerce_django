from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from account.models import Account
import json
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Order

class AddToOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product')
        access_expiry_date = request.data.get('access_expiry_date', None)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        order, created = Order.objects.get_or_create(customer=user, status=False)

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            access_expiry_date=access_expiry_date
        )

        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user , status=False)
