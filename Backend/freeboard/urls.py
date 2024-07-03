from django.urls import path, include
from .views import FreeboardPostModelViewSet, FreeboardPostCommentModelViewSet
from rest_framework import routers


# URL = freeboard/ 로 시작, 기본 라우터 설정
app_name = 'freeboard'
router = routers.DefaultRouter()

# 자유게시판 ViewSet Router
router.register(r'post', FreeboardPostModelViewSet)

# 자유게시판 댓글 Viewset url 연결
router.register(r'comment', FreeboardPostCommentModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]