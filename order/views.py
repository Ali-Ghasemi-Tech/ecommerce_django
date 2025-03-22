from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
<<<<<<< HEAD
from products.models import Product
=======
from account.models import Account
# add
import json
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Order
>>>>>>> my-new-branch

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
<<<<<<< HEAD
        return Order.objects.filter(customer=self.request.user , status=False)
=======
        user = self.request.user
        return Order.objects.filter(customer=user , status=False)


class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_item_id = self.kwargs.get('order_item_id')
        return get_object_or_404(OrderItem, id=order_item_id, order__customer=self.request.user)


# # درگاه بانکی 


# # ویو برای ایجاد درخواست پرداخت
# def request_payment(request):
#     try:
#         # Replace 'amount' with the correct logic for creating an Order
#         order = Order.objects.create(
#             customer=request.user.account,  # Assuming the user is logged in and has an Account
#             status=False  # Default to unpaid
#         )

#         zarinpal_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
#         callback_url = "http://127.0.0.1:8000/verify/"

#         data = {
#             "MerchantID": settings.ZARINPAL_MERCHANT_ID,
#             "Amount": 10000,  # مقدار پرداخت (مثلاً ۱۰ هزار تومان)
#             "Description": f"پرداخت سفارش شماره {order.id}",
#             "CallbackURL": callback_url,
#         }

#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(zarinpal_url, data=json.dumps(data), headers=headers)

#         if response.status_code == 200:
#             res_data = response.json()
#             if res_data["Status"] == 100:
#                 order.authority = res_data["Authority"]
#                 order.save()
#                 return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{res_data['Authority']}")

#     except Exception as e:
#         return HttpResponse("خطایی در ایجاد درخواست پرداخت رخ داده است!")

#     return HttpResponse("خطایی در ایجاد درخواست پرداخت رخ داده است!")

# # ویو برای بررسی وضعیت پرداخت
# def verify_payment(request):
#     authority = request.GET.get("Authority")
#     order = Order.objects.filter(authority=authority).first()

#     if not order:
#         return HttpResponse("سفارش پیدا نشد!")

#     zarinpal_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"

#     data = {
#         "MerchantID": settings.ZARINPAL_MERCHANT_ID,
#         "Amount": order.amount,
#         "Authority": authority,
#     }

#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(zarinpal_url, data=json.dumps(data), headers=headers)

#     if response.status_code == 200:
#         res_data = response.json()
#         if res_data["Status"] == 100:
#             order.status = 'paid'
#             order.save()
#             return HttpResponse(f"پرداخت موفقیت‌آمیز بود! کد تراکنش: {res_data['RefID']}")
#         else:
#             order.status = 'failed'
#             order.save()
#             return HttpResponse("پرداخت ناموفق بود!")

#     return HttpResponse("خطا در بررسی پرداخت!")
>>>>>>> my-new-branch
