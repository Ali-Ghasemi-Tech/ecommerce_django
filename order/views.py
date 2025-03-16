from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from account.models import Account


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the user has an existing unpaid order
        order, created = Order.objects.get_or_create(customer=user, status=False)

        # Create or update the order item
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            # If the item already exists in the order, you can update the quantity or other fields if needed
            product.units_sold += 1 

        # Recalculate the total price of the order
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)


class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_item_id = self.kwargs.get('order_item_id')
        return get_object_or_404(OrderItem, id=order_item_id, order__customer=self.request.user)
