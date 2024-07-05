from django.urls import path, include
from .views import *
from rest_framework import routers

# URL = freeboard/ 로 시작
app_name = 'accounts/kakao/'

urlpatterns = [
    path('accounts/kakao/login/', kakao_login, name='kakao_login'),
    path('accounts/kakao/callback/', kakao_callback, name='kakao_callback'),
    path('accounts/kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
    
]