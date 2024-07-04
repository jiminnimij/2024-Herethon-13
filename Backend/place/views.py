from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from .models import Review, Place, WomenOnlyPlace
from .serializers import ReviewSerializer, PlaceSerializer, WomenOnlyPlaceSerializer

# Create your views here.

# 리뷰 뷰셋
class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

# 장소 뷰셋
class PlaceViewSet(ModelViewSet):
    queryset=Place.objects.all()
    serializer_class=PlaceSerializer

# 여성 전용 시설 뷰셋
class WomenOnlyPlaceViewSet(ModelViewSet):
    queryset=WomenOnlyPlace.objects.all()
    serializer_class=WomenOnlyPlaceSerializer

    # 카테고리로 검색 필드 설정
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['women_only_category']