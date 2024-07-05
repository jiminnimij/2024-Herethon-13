from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

# URL = freeboard/ 로 시작
app_name = 'accounts/kakao/'
router = routers.DefaultRouter()

router.register(r'profile', Profile, basename='profile')

urlpatterns = [
    path('login/', kakao_login, name='kakao_login'),
    path('callback/', kakao_callback, name='kakao_callback'),
    path('login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
    # path('logout/', kakao_logout, name='kakao_logout'),
    path('', include(router.urls)),
    path("auth/refresh/", TokenRefreshView.as_view()),
    
]