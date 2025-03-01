from .serializers import SignupSerializer , UpdateSerializer , LoginSerializer, MemberSerializer
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateAPIView , RetrieveDestroyAPIView , RetrieveAPIView , ListAPIView
from rest_framework import status , permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MemberModel , Profile
from django.conf import settings
from django.core.mail import send_mail
from .backends import MemberAuthBackend
from .permissions import IsSuperUserOrSelf
from django.shortcuts import get_object_or_404

class SignupApiView(ListCreateAPIView):
    queryset = MemberModel.objects.all()
    serializer_class = SignupSerializer
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create a profile and generate a verification token
            profile = Profile.objects.create(user=user)
            token = profile.generate_verification_token()

            # Send verification email
            verification_link = f"http://127.0.0.1:8000/members/api/verify-email/{token}/"
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "User registered successfully. Check your email for verification."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyEmailView(APIView):
    def get(self, token):
        profile = get_object_or_404(Profile, email_verification_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

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
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
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
