from rest_framework import viewsets, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # نیاز به ورود دارد

    def get_queryset(self):
        # فقط سفارشات کاربر لاگین‌شده را برمی‌گرداند
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """API برای کنسل کردن سفارش"""
        order = get_object_or_404(Order, pk=pk, user=request.user)
        order.status = "canceled"
        order.save()
        return Response({"message": "Order canceled successfully"})
