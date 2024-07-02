from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import FreeboardPost
from .serializers import FreeboardPostModelSerializer

# Create your views here.
class FreeboardPostModelViewSet(ModelViewSet):
    queryset=FreeboardPost.objects.all()
    serializer_class=FreeboardPostModelSerializer