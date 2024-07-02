from django.urls import path, include
from .views import FreeboardPostModelViewSet
from rest_framework import routers

# URL = freeboard/ 로 시작
app_name = 'freeboard'

# ViewSet Router
router = routers.DefaultRouter()
router.register('', FreeboardPostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]