from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['email','kakao_oid','nickname','gender','age_range','profile_image','password']

  def update(self, instance, validated_data):
    instance.gender = validated_data.get('gender', instance.gender)
    instance.age_range = validated_data.get('age_range', instance.age_range)
    instance.profile_image = validated_data.get('profile_image', instance.profile_image)
    instance.nickname = validated_data.get('nickname', instance.nickname)
    instance.kakao_oid = validated_data.get('kakao_oid', instance.kakao_oid)
    instance.save()
    return instance