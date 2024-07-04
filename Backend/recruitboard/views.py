from rest_framework.viewsets import ModelViewSet

from .models import RecruitboardPost
from .serializers import RecruitboardPostModelSerializer

# Create your views here.

# 채용게시판 게시글 뷰셋
class RecruitboardPostModelViewSet(ModelViewSet):
    queryset=RecruitboardPost.objects.all()
    serializer_class=RecruitboardPostModelSerializer