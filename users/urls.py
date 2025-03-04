from django.urls import path , include
from .views import  SignupApiView , UpdateApiView ,MemberLoginView , DeleteApiView , DetailApiView , MemberListApiView , VerifyEmailView , VerifyPhoneView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns =[
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/' , SignupApiView.as_view() , name='signup_api'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/verify-phone/', VerifyPhoneView.as_view(), name='verify_phone'),
    path('api/login/' , MemberLoginView.as_view() , name='login_api'),
    path('api/memberslist/' , MemberListApiView.as_view() , name = 'member_list'),
    path('api/<int:pk>/update/' , UpdateApiView.as_view() , name= 'update_api'),
    path('api/<int:pk>/remove/' , DeleteApiView.as_view() , name = 'delete_api'),
    path('api/<int:pk>/detail/' , DetailApiView.as_view() , name='detail_api'),
]