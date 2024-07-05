from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from .models import FreeboardPost, FreeboardPostComment
from .serializers import FreeboardPostModelSerializer, FreeboardPostCommentModelSerializer

# Create your views here.

# 자유게시판 게시글 뷰셋
class FreeboardPostModelViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset=FreeboardPost.objects.all()
    serializer_class=FreeboardPostModelSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

# 자유게시판 댓글 뷰셋
class FreeboardPostCommentModelViewSet(ModelViewSet):
    queryset=FreeboardPostComment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset=FreeboardPostComment.objects.all()
    serializer_class=FreeboardPostCommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

