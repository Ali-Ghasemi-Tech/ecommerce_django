# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from django.shortcuts import redirect
from .models import PaymentTransaction
from .serializers import PaymentInitiateSerializer
from order.models import Order
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

class InitiatePaymentView(APIView):
    """
    Handles payment initiation through POST request
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication] 

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if serializer.is_valid():
            merchant_id = settings.ZARINPAL_MERCHANT_ID
            amount = serializer.validated_data['amount']
            order_id = serializer.validated_data['order_id']
            order = Order.objects.get(pk = order_id)
            user = request.user
            description = f'Payment for order {order_id}'
            
            callback_url = request.build_absolute_uri('/api/payment/verify/')
            print(user)
            request_data = {
                "merchant_id": merchant_id,
                "amount": amount,
                "description": description,
                "callback_url": callback_url,
                "metadata": {
                    "mobile": user.phone_number,
                }
            }

            # Send request to ZarinPal
            response = requests.post(
                'https://sandbox.zarinpal.com/pg/v4/payment/request.json',
                json=request_data,
                headers={'accept': 'application/json', 'content-type': 'application/json'}
            )

            if response.status_code == 200:

                response_data = response.json()

                if response_data['data']['code'] == 100:
                    
                    authority = response_data['data']['authority']
                    
                    # Create transaction record
                    PaymentTransaction.objects.create(
                        order= order,
                        user=user,
                        amount=amount,
                        authority=authority,
                        status='pending'
                    )
                    
                    return Response({
                        'payment_url': f'https://sandbox.zarinpal.com/pg/StartPay/{authority}',
                        'authority': authority
                    }, status=status.HTTP_200_OK)
                    
                return Response(
                    {'error': response_data.get('errors', {'message': 'Unknown error'})},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(
                {'error': 'Payment gateway connection failed'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    """
    Handles payment verification callback from ZarinPal
    """
    def get(self, request):
        authority = request.GET.get('Authority')
        status_param = request.GET.get('Status', 'NOK')
        
        if status_param == 'OK':
            try:
                transaction = PaymentTransaction.objects.get(authority=authority)
            except PaymentTransaction.DoesNotExist:
                return redirect(f'{settings.FRONTEND_URL}/payment/error?error=Transaction not found')

            verification_data = {
                "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                "amount": transaction.amount,
                "authority": authority
            }

            # Verify payment with ZarinPal
            verify_response = requests.post(
                'https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
                json=verification_data,
                headers={'accept': 'application/json', 'content-type': 'application/json'}
            )

            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                if verify_data.get('data').get('code') == 100:
                    transaction.status = 'success'
                    transaction.save()
                    return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
                
                transaction.status = 'failed'
                transaction.save()
                error = verify_data.get('errors', {'message': 'Verification failed'})
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            transaction.status = 'failed'
            transaction.save()
            return Response({'error': 'Payment gateway connection failed'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({'error': 'Payment was not successful'}, status=status.HTTP_400_BAD_REQUEST)