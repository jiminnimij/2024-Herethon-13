from django.urls import path, include
from .views import RecruitboardPostModelViewSet
from rest_framework import routers


# URL = recruitboard/ 로 시작, 기본 라우터 설정
app_name = 'recruitboard'
router = routers.DefaultRouter()

# 재용게시판 ViewSet Router
router.register(r'', RecruitboardPostModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]