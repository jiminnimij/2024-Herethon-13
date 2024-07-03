from rest_framework.serializers import ModelSerializer
from .models import FreeboardPost, FreeboardPostComment


class FreeboardPostCommentModelSerializer(ModelSerializer):
    class Meta:
        model = FreeboardPostComment
        fields = '__all__'

class FreeboardPostModelSerializer(ModelSerializer):
    comments = FreeboardPostCommentModelSerializer(many=True, read_only=True, source='freeboardpostcomment_set')

    class Meta:
        model = FreeboardPost
        fields = '__all__'

