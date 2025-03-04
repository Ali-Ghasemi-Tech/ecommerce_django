from django.urls import path , include
from .views import  SignupApiView , UpdateApiView , LoginApiView , DeleteApiView , DetailApiView , MemberListApiView , VerifyEmailView
urlpatterns =[
    path('' , include('rest_framework.urls')),
    path('api/signup/' , SignupApiView.as_view() , name='signup_api'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),

    path('api/login/' , LoginApiView.as_view() , name='login_api'),
    path('api/memberslist/' , MemberListApiView.as_view() , name = 'member_list'),
    path('api/<int:pk>/update/' , UpdateApiView.as_view() , name= 'update_api'),
    path('api/<int:pk>/remove/' , DeleteApiView.as_view() , name = 'delete_api'),
    path('api/<int:pk>/detail/' , DetailApiView.as_view() , name='detail_api'),
]