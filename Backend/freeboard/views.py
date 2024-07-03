from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import FreeboardPost, FreeboardPostComment
from .serializers import FreeboardPostModelSerializer, FreeboardPostCommentModelSerializer

# Create your views here.

# 자유게시판 게시글 뷰셋
class FreeboardPostModelViewSet(ModelViewSet):
    queryset=FreeboardPost.objects.all()
    serializer_class=FreeboardPostModelSerializer


# 자유게시판 댓글 뷰셋
class FreeboardPostCommentModelViewSet(ModelViewSet):
    queryset=FreeboardPostComment.objects.all()
    serializer_class=FreeboardPostCommentModelSerializer