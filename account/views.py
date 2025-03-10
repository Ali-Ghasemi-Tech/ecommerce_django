from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateAPIView
from rest_framework import status , viewsets , permissions
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from kavenegar import *
from .models import Account , Profile
from .serializers import SignupSerializer , LoginSerializer , PasswordChangeSerializer , AccountUpdateSerializer
from rest_framework.views import APIView
from .serializers import VerifyPhoneSerializer
from django.contrib.auth import authenticate, login , logout
from rest_framework.decorators import action



def handle_phone_api(user):
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = Profile.objects.create(user=user)
    code = profile.generate_phone_verification_token()

    try:
        api = KavenegarAPI('32354D4E2F3631306B4C796D5861574E4D5970634346497034614A463555424F774E3536472B46685545383D')
        params = { 'sender' : '2000660110', 'receptor': f'{user.phone_number}', 'message' :f'برای تایید شماره تلفن خود، کد زیر را در سایت واردکنید: {code}' }
        response = api.sms_send(params)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

class SignupApiView(ListCreateAPIView):
    serializer_class = SignupSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Account.objects.all()
        else:
            try:
                return Account.objects.get(pk = self.request.user.id)
            except Account.DoesNotExist:
                return Account.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            handle_phone_api(user)  # Your existing phone verification logic
            return Response({'redirect': reverse('verify_phone')}, status=status.HTTP_201_CREATED)
          
        return Response( status=status.HTTP_400_BAD_REQUEST)
    

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
        

class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')


        user = authenticate(request, username=username, password=password)
 

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