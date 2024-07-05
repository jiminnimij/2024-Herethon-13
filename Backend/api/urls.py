from django.urls import path, include
from .views import *
from rest_framework import routers

# URL = freeboard/ 로 시작
app_name = 'accounts/kakao/'

urlpatterns = [
    path('login/', kakao_login, name='kakao_login'),
    path('callback/', kakao_callback, name='kakao_callback'),
    path('login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('profile/', Profile.as_view(), name = "kakao_profile")
    
]