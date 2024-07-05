from .serializers import *
import os
from urllib import request
from django.views import View
import requests
from rest_framework.response import Response

from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.conf import settings
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse

from json.decoder import JSONDecodeError

import logging
logger = logging.getLogger(__name__)

KAKAO_CALLBACK_URI = "http://127.0.0.1:8000"
def kakao_login(request):
    rest_api_key = getattr(settings, '')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

def kakao_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")

    # code로 access token 요청
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
    token_response_json = token_request.json()

    # 에러 발생 시 중단
    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    profile_json = profile_request.json()

    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None) # 이메일!

    # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함
    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status = status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(email=email)

    user.kakao_oid = profile_json.get("id")
    user.gender = kakao_account.get("gender")

    if kakao_account.get("profile_nickname_needs_agreement"):
        user.username = kakao_account["profile"]["nickname"]

    if kakao_account.get("profile_image_needs_agreement"):
        user.profile_image = kakao_account["profile"]["profile_image_url"]
    
    if kakao_account.get("age_range_needs_agreement"):
        user.age_range = kakao_account.get("age_range")

    user.save()

    return JsonResponse({'message': 'Kakao login success', 'access_token': access_token}, status=status.HTTP_200_OK)

#    
class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


