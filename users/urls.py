from django.urls import path , include
from . import views
urlpatterns =[
    path('' , include('rest_framework.urls')),
    path('api/signup/' , views.SignupApiView.as_view() , name='signup_api'),
    path('api/verify-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('api/verify-phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('api/login/' , views.LoginApiView.as_view() , name='login_api'),
    path('api/logout/' , views.LogoutApiView.as_view() , name= 'logout_api'),
    path('api/memberslist/' , views.MemberListApiView.as_view() , name = 'member_list'),
    path('api/<int:pk>/update/' , views.UpdateApiView.as_view() , name= 'update_api'),
    path('api/<int:pk>/remove/' , views.DeleteApiView.as_view() , name = 'delete_api'),
    path('api/<int:pk>/detail/' , views.DetailApiView.as_view() , name='detail_api'),
]