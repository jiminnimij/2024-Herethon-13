from rest_framework.serializers import ModelSerializer
from .models import RecruitboardPost


class RecruitboardPostModelSerializer(ModelSerializer):
    class Meta:
        model = RecruitboardPost
        fields = '__all__'

