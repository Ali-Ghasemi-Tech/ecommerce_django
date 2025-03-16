from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateAPIView
from rest_framework import status , viewsets , permissions
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
        verification_link = f"http://127.0.0.1:8000/members/api/verify-email/{token}/"
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

class SignupApiView(ListCreateAPIView):
    serializer_class = SignupSerializer

    # remove for production
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Account.objects.all()
        else:
            try:
                return []
            except Account.DoesNotExist:
                return []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send verification code to user (email or phone)
            if serializer.validated_data['phone_number'] and serializer.validated_data['email']:
                handle_phone_api(user)
                handle_email_api(user)
                profile = Profile.objects.get(user=user)
                return redirect(reverse("verify_phone", kwargs={"verification_uuid": profile.verification_uuid}))
            
            elif serializer.validated_data['phone_number']:
                handle_phone_api(user) 
                profile = Profile.objects.get(user=user)
                return redirect(reverse("verify_phone", kwargs={"verification_uuid": profile.verification_uuid}))
            
            elif serializer.validated_data['email']:
                handle_email_api(user)
                Response({'message' : "vrificatin link has been sent to your email"} , status=status.HTTP_200_OK)

            
            
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    def get(self, token):
        profile = get_object_or_404(Profile, email_verification_token=token)
        user = profile.user
        user.email_verified = True
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
                user.phone_verified = True
                user.is_active = True
                user.save()
                return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            
            return Response({"error": f"Invalid token {token}"}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginApiView(APIView):
    serializer_class = LoginSerializer

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
                return Response({'error': 'Invalid credentials or phone not verified'}, status=status.HTTP_401_UNAUTHORIZED)

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