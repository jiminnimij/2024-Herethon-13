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
#     rest_api_key = getattr(settings, 'c46ab624868aee506356e4c765243e8a')
#     code = request.GET.get("code")
#     redirect_uri = KAKAO_CALLBACK_URI
#     """
#     Access Token Request
#     """
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get("access_token")
#     """
#     Email Request
#     """
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
#     profile_json = profile_request.json()
#     kakao_account = profile_json.get('kakao_account')
#     """
#     kakao_account에서 이메일 외에
#     카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
#     print(kakao_account) 참고
#     """
#     # print(kakao_account)
#     email = kakao_account.get('email')
#     """
#     Signup or Signin Request
#     """
#     try:
#         user = CustomUser.objects.get(email=email)
#         # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'kakao':
#             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
#         # 기존에 Google로 가입된 유저
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"http://127.0.0.1:8000/accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#     except CustomUser.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"http://127.0.0.1:8000/accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#         # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
# class KakaoLogin(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    data = {
        "grant_type":"authorization_code",
        "client_id": client_id,
        "redirection_url" :KAKAO_CALLBACK_URI,
        "code":code
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = request.post(kakao_token_api, data=data).json()["access_token"]
    # code로 access token 요청
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
    token_response_json = token_request.json()

    # 에러 발생 시 중단
    error = token_response_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    profile_json = profile_request.json()

    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email")
    kakao_oid = profile_json.get("id")

    gender = kakao_account.get("gender")
    if gender.lower() != "female":
        raise JSONDecodeError(error)

    if kakao_account.get("profile_nickname_needs_agreement"):
        nickname = kakao_account["profile"]["nickname"]

    if kakao_account.get("profile_image_needs_agreement"):
        profile_image = kakao_account["profile"]["profile_image_url"]
    
    if kakao_account.get("age_range_needs_agreement"):
        age_range = kakao_account.get("age_range")

    try:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"http://127.0.0.1:8000/accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        cookie_max_age = 3600 * 24 * 14 # 14 days
        refresh_token = refresh_token[token_index+1]
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie
    
    except CustomUser.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"http://127.0.0.1:8000/accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        user = CustomUser.objects.create(
        email=email,
        kakao_oid=kakao_oid,
        gender=gender,
        nickname=nickname,
        profile_image=profile_image,
        age_range=age_range
        )
        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        refresh_token = refresh_token[token_index+1]

        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie

    #이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함



    # user, created = CustomUser.objects.get_or_create(email=email)

    

    # user.save()

    return JsonResponse({'message': 'Kakao login success', 'access_token': access_token}, status=status.HTTP_200_OK)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


# from json import JSONDecodeError
# import os
# import requests
# from rest_framework import status
# from django.http import JsonResponse
# from django.shortcuts import redirect
# from .models import CustomUser
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.kakao import views as kakao_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# KAKAO_CALLBACK_URI ='http://127.0.0.1:8000/accounts/kakao/login/callback/'

# def kakao_login(request):
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email%20profile%20nickname%20gender%20age_range")

# def kakao_callback(request):
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     code = request.GET.get("code")

#     # code로 access token 요청
#     token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
#     token_response_json = token_request.json()

#     # 에러 발생 시 중단
#     error = token_response_json.get("error", None)
#     if error is not None:
#         raise JSONDecodeError(error)

#     access_token = token_response_json.get("access_token")

#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )

#     profile_json = profile_request.json()

#     kakao_account = profile_json.get("kakao_account")
#     email = kakao_account.get("email", None) # 이메일!

#     # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함
#     if email is None:
#         return JsonResponse({'err_msg': 'failed to get email'}, status = status.HTTP_400_BAD_REQUEST)

#     user, created = CustomUser.objects.get_or_create(email=email)

#     user.kakao_oid = profile_json.get("id")
#     user.gender = kakao_account.get("gender")

#     if kakao_account.get("profile_nickname_needs_agreement"):
#         user.username = kakao_account["profile"]["nickname"]

#     if kakao_account.get("profile_image_needs_agreement"):
#         user.profile_image = kakao_account["profile"]["profile_image_url"]
    
#     if kakao_account.get("age_range_needs_agreement"):
#         user.age_range = kakao_account.get("age_range")

#     user.save()

#     return JsonResponse({'message': 'Kakao login success', 'access_token': access_token}, status=status.HTTP_200_OK)

# class KakaoLogin(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     callback_url = KAKAO_CALLBACK_URI
#     client_class = OAuth2Client


# from json import JSONDecodeError
# import os
# from rest_framework import status
# from django.http import JsonResponse
# from django.shortcuts import redirect
# from .models import CustomUser
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.kakao import views as kakao_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# import requests

# KAKAO_CALLBACK_URI ='http://127.0.0.1:8000/accounts/kakao/login/callback/'

# def kakao_login(request):
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email")

# def kakao_callback(request):
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     code = request.GET.get("code")

#     # code로 access token 요청
#     token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
#     token_response_json = token_request.json()

#     # 에러 발생 시 중단
#     error = token_response_json.get("error", None)
#     access_token = token_response_json.get("access_token")
#     if error is not None:
#         raise JSONDecodeError(error)
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )

#     profile_json = profile_request.json()

#     kakao_account = profile_json.get("kakao_account")
#     email = kakao_account.get("email", None) # 이메일!

#     # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함
#     if email is None:
#         return JsonResponse({'err_msg': 'failed to get email'}, status = status.HTTP_400_BAD_REQUEST)
#     # access_token = token_response_json.get("access_token")
#     user, created = CustomUser.objects.get_or_create(email=email)

#     user.kakao_oid = profile_json.get("id")
#     kakao_account = profile_json.get("kakao_account")
#     if kakao_account.get("gender","").lower() !="female":
#         return JsonResponse({'err_msg': 'reject'}, status = status.HTTP_400_BAD_REQUEST)
#     else:
#         user.gender = kakao_account.get("gender")

#     if kakao_account.get("profile_nickname_needs_agreement"):
#         user.username = kakao_account["profile"]["nickname"]

#     if kakao_account.get("profile_image_needs_agreement"):
#         user.profile_image = kakao_account["profile"]["profile_image_url"]
    
#     if kakao_account.get("age_range_needs_agreement"):
#         user.age_range = kakao_account.get("age_range")

#     user.save()

#     return JsonResponse({'message': 'Kakao login success', 'access_token': access_token}, status=status.HTTP_200_OK)

# class KakaoLogin(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     callback_url = KAKAO_CALLBACK_URI
#     client_class = OAuth2Client
# from json import JSONDecodeError

# from django.http import JsonResponse
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.kakao import views as kakao_view

# def kakao_callback(request):
#     code = request.GET.get("code")
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     # Access Token Request
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
#     )

#     token_req_json = token_req.json()

#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)

#     access_token = token_req_json.get("access_token")

#     # Email Request
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()

#     kakao_oid = profile_json.get("id")
#     gender = kakao_account.get("gender")
#     kakao_account = profile_json.get("kakao_account")
#     username = kakao_account["profile"]["nickname"]
#     profile_image_url = kakao_account["profile"]["profile_image_url"]
#     email = kakao_account.get("email")
    
#     age = kakao_account.get("age_range")

#     data = {"access_token": access_token, "code": code}
#     # TODO 유저 프로필 이미지 저장하도록
#     return JsonResponse(data)

# class KakaoLoginView(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI