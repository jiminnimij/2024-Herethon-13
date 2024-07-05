from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['email','kakao_oid','nickname','gender','age_range','profile_image','password']