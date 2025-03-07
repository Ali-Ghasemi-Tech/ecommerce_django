from .serializers import SignupSerializer , UpdateSerializer , LoginSerializer, MemberSerializer , VerifyPhoneSerializer
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateAPIView , RetrieveDestroyAPIView , RetrieveAPIView , ListAPIView
from rest_framework import status , permissions
from rest_framework.response import Response 
from rest_framework.views import APIView
from .models import MemberModel , Profile
from django.conf import settings
from django.core.mail import send_mail
from .backends import MemberAuthBackend
from .permissions import IsSuperUserOrSelf
from django.shortcuts import get_object_or_404 ,redirect
from kavenegar import *
from .forms import VerifyPhoneForm
from django.urls import reverse 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout

def handle_phone_api(user):
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = Profile.objects.create(user=user)
    code = profile.generate_phone_verification_token()

    try:
        api = KavenegarAPI('32354D4E2F3631306B4C796D5861574E4D5970634346497034614A463555424F774E3536472B46685545383D')
        params = { 'sender' : '2000660110', 'receptor': '09212155738', 'message' :f'برای تایید شماره تلقن خود کد زیر را در سابت واردکنید: {code}' }
        response = api.sms_send(params)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)


# add phone verification

class SignupApiView(ListCreateAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = SignupSerializer
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            handle_phone_api(user)
            # Create a profile and generate a verification token
            # token = profile.generate_verification_token()

            # Send verification email

            # verification_link = f"http://127.0.0.1:8000/members/api/verify-email/{token}/"
            # send_mail(
            #     'Verify your email',
            #     f'Click the link to verify your email: {verification_link}',
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            # )

            return redirect(reverse('verify_phone'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyEmailView(APIView):
    def get(self, token):
        profile = get_object_or_404(Profile, email_verification_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
    
class VerifyPhoneView(APIView):
    serializer_class = VerifyPhoneSerializer
    def post(self, request):
        serializer = VerifyPhoneSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        token = serializer.validated_data['token']
        try:
            profile = Profile.objects.get(phone_verification_token=token)
            user = profile.user
            user.is_active = True
            user.save()
            return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            
            return Response({"error": f"Invalid token {token}"}, status=status.HTTP_400_BAD_REQUEST)
        
        

class UpdateApiView(RetrieveUpdateAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = UpdateSerializer

class LoginApiView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = MemberAuthBackend.authenticate(request, username=username, password=password)

        if user:
            # Authentication successful
            login(request , user , backend= 'users.backends.MemberAuthBackend')
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutApiView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)  # Destroys the session
            return Response({'message': 'success'} , status=status.HTTP_200_OK)
        else:
            return Response({'message': 'not logged in'}, status=status.HTTP_400_BAD_REQUEST)

        
class DeleteApiView(RetrieveDestroyAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsSuperUserOrSelf]

class DetailApiView(RetrieveAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsSuperUserOrSelf]

class MemberListApiView(ListAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAdminUser]
