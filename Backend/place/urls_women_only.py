from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WomenOnlyPlaceViewSet

# 기본 라우터 설정
app_name = 'womenonly'
router = SimpleRouter()

# 장소 ViewSet url 연결
router.register(r'place', WomenOnlyPlaceViewSet, basename='place')

urlpatterns = [
    path('', include(router.urls)),
]
