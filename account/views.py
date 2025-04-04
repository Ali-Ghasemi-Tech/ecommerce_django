from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateAPIView ,CreateAPIView
from rest_framework import status , viewsets , permissions , exceptions , views
from rest_framework.response import Response
from django.shortcuts import redirect , get_object_or_404
from django.urls import reverse
from kavenegar import *
from .models import Account , Profile
from .serializers import SignupSerializer , LoginSerializer , PasswordChangeSerializer , AccountUpdateSerializer
from rest_framework.views import APIView
from .serializers import VerifyPhoneSerializer
from django.contrib.auth import authenticate, login , logout
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail

def handle_email_api(user):
    try:
        profile = Profile.objects.get(user=user)
        token = profile.generate_verification_token()
        verification_link = f"http://127.0.0.1:8000/api/account/verify-email/{token}/"
        send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        )
    except Exception:
        Response({'message':'there was a problem with sending the email'} , status=status.HTTP_503_SERVICE_UNAVAILABLE)


def handle_phone_api(user):
    try:
        profile = Profile.objects.get(user=user)
        code = profile.phone_verification_token
    except:
        profile = Profile.objects.create(user=user)
        code = profile.generate_phone_verification_token()

    try:
        api = KavenegarAPI('32354D4E2F3631306B4C796D5861574E4D5970634346497034614A463555424F774E3536472B46685545383D')
        params = { 'sender' : '2000660110', 'receptor': f'{user.phone_number}', 'message' :f'برای تایید شماره تلفن خود، کد زیر را در سایت واردکنید: {code}' }
        api.sms_send(params)
        profile.expire = timezone.now() + timezone.timedelta(minutes=6)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

class SignupApiView(views.APIView):
    
    
    def get_serializer_context(self):
        return {"request": self.request}
   
    def get_serializer(self, data, *args, **kwargs):
        return SignupSerializer(data=data, context=self.get_serializer_context())
    
    def get_serializer_context(self):
        # Pass request context to serializer (e.g., for URL building)
        return {"request": self.request}
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send verification code to user (email or phone)
            if serializer.validated_data['phone_number'] and serializer.validated_data['email']:
                handle_phone_api(user)
                handle_email_api(user)
                profile = Profile.objects.get(user=user)
                return Response({
                        "message": "کذ تایید به شماره تلفنی که وارد کردید ارسال شد و لینک تایید به ایمیلتان ارسال شد",
                        "verification_uuid": str(profile.verification_uuid),
                        "next_step": "verify_phone"  
                    }, status=status.HTTP_200_OK)             
            elif serializer.validated_data['phone_number']:
                handle_phone_api(user) 
                profile = Profile.objects.get(user=user)
                return Response({
                        "message": "کذ تایید به شماره تلفنی که وارد کردید ارسال شد",
                        "verification_uuid": str(profile.verification_uuid),
                        "next_step": "verify_phone"  
                    }, status=status.HTTP_200_OK)            
            elif serializer.validated_data['email']:
                handle_email_api(user)
                Response({'message' : "لینک تایید به ایمیلتان ارسال شد"} , status=status.HTTP_200_OK)

            
            
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    lookup_url_kwargs = 'token'
    def get(self, token):
        print(token)
        profile = get_object_or_404(Profile, email_verification_token=token)
        user = profile.user
        user.email_active = True
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)


class VerifyPhoneView(APIView):
    serializer_class = VerifyPhoneSerializer
    lookup_url_kwargs = 'verification_uuid'
    
    def post(self, request , verification_uuid):
        serializer = VerifyPhoneSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        token = serializer.validated_data['token']
        try:
            profile = Profile.objects.get(phone_verification_token=token ,verification_uuid=verification_uuid)
            
          
            if profile.expire < timezone.now():
                profile.delete()
                return Response({"error": "Token expired , request for another one"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = profile.user
                user.phone_number_active = True
                user.is_active = True
                user.save()
                return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            
            return Response({"error": f"Invalid token {token}"}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginApiView(views.APIView):


   
    def get_serializer(self, data, *args, **kwargs):
        return LoginSerializer(data=data, context=self.get_serializer_context())
    
    def get_serializer_context(self):
        return {"request": self.request}
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone_or_username = serializer.validated_data['email_or_phone_or_username']
            password = serializer.validated_data['password']


            user = authenticate(request, username=email_or_phone_or_username, password=password)
    

            if user:
                # Authentication successful
                login(request , user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'اطلاعات وارد شده صحیح نمیباشند یا شماره تلفن خود را تایید نکردید'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'the form is not valid'} , status=status.HTTP_400_BAD_REQUEST)

class UpdateApiView(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer


class LogoutApiView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)  # Destroys the session
            return Response({'message': 'success'} , status=status.HTTP_200_OK)
        else:
            return Response({'message': 'not logged in'}, status=status.HTTP_400_BAD_REQUEST)