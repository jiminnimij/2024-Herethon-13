from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ReviewViewSet, PlaceViewSet, ScrapViewSet

# 기본 라우터 설정
app_name = 'place'
router = SimpleRouter()

# 장소 ViewSet url 연결
router.register(r'place', PlaceViewSet, basename='place')

# 리뷰 Viewset url 연결
router.register(r'review', ReviewViewSet, basename='review')

# 스크랩 Viewset url 연결
router.register(r'scrap', ScrapViewSet, basename='scrap')

urlpatterns = [
    path('', include(router.urls)),
]
