from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product, CartItem, Order, Payment, OrderItem
from django.contrib.auth.decorators import login_required
from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from .serializers import CartSerializer, OrderSerializer, PaymentSerializer, OrderItemSerializer, CartItemListSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all().order_by('-created_at')
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]  # نیاز به ورود دارد

# class CartAPIView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         try:
#             cart = Cart.objects.get(user=self.request.user)
#             return cart
#         except Exception as e:
#             return None
            

#     def get(self, request):
#         serializer = CartSerializer(self.get_queryset())
#         return Response(serializer.data)

#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         cart_item.quantity += 1
#         cart_item.save()
#         return Response({'status': 'Product added to cart'})

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return Response({'status': 'Product added to cart'} )

class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return Response({'status': 'Product removed from cart'})

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        payment = Payment.objects.create(order=order, amount=order.total_price, payment_method='credit_card', status='completed')
        order.status = 'paid'
        order.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class CartAPIView(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return CartItem.objects.filter(cart = cart)
    
    def list(self, request, *args, **kwargs):
        try:
            query_set = self.get_queryset()
            serializer = self.get_serializer(query_set , many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':f'{str(e)}'} , status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            self.perform_destroy(item)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f'{str(e)}'} , status=status.HTTP_400_BAD_REQUEST)
    
    
