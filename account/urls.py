from django.contrib import admin
from django.urls import path , include
from . import views



urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('signup/', views.SignupApiView.as_view(), name='signup'),
    path('verify_phone/', views.VerifyPhoneView.as_view(), name='verify_phone'),
    path('login/' , views.LoginApiView.as_view() , name='login_api'),
    path('logout/' , views.LogoutApiView.as_view() , name= 'logout_api'),
    # path('memberslist/' , views.MemberListApiView.as_view() , name = 'member_list'),
    path('<int:pk>/update/' , views.UpdateApiView.as_view() , name= 'update_api'),
    # path('<int:pk>/remove/' , views.DeleteApiView.as_view() , name = 'delete_api'),
    # path('<int:pk>/detail/' , views.DetailApiView.as_view() , name='detail_api'),
]