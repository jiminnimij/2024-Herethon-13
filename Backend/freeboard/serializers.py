from rest_framework.serializers import ModelSerializer
from .models import FreeboardPost

class FreeboardPostModelSerializer(ModelSerializer):
    class Meta:
        model = FreeboardPost
        fields = '__all__'