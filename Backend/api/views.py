from json import JSONDecodeError
import os
from django.views import View
import requests
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

from .serializers import UserSerializer
from .models import CustomUser
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

KAKAO_CALLBACK_URI ='http://127.0.0.1:8000/accounts/kakao/login/callback/'
BASE_URL = 'http://127.0.0.1:8000/'
def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")


# def kakao_callback(request):
#     client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
#     client_secret = os.environ.get("SOCIAL_AUTH_KAKAO_SECRET")
#     code = request.GET.get("code")

#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'redirect_uri': KAKAO_CALLBACK_URI,
#         'code': code,
#     }

#     headers = {
#         'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
#     }

#     token_url = 'https://kauth.kakao.com/oauth/token'

#     # code로 access token 요청
#     token_response = requests.post(token_url, headers=headers, data=data)
#     token_response_json = token_response.json()
#     print("Token response:", token_response_json)

#     # 에러 발생 시 중단
#     error = token_response_json.get("error", None)
#     if error is not None:
#         return JsonResponse({'err_msg': error}, status=status.HTTP_400_BAD_REQUEST)

#     access_token = token_response_json.get("access_token")
#     if access_token is None:
#         return JsonResponse({'err_msg': 'failed to get access token'}, status=status.HTTP_400_BAD_REQUEST)

#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()

#     kakao_account = profile_json.get("kakao_account")
#     email = kakao_account.get("email", None)
#     if email is None:
#         return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # try:
#     #     user = CustomUser.objects.get(email=email)

#     #     data = {'access_token': access_token, 'code': code}
#     #     accept = requests.post(f"https://127.0.0.1:8000/accounts/kakao/login/finish/", data=data)
#     #     accept_status = accept.status_code

#     #     if accept_status != 200:
#     #         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
#     #     accept_json = accept_json()
#     #     accept_json.pop('user',None)
#     #     return JsonResponse(accept_json)

#     # except CustomUser.DoesNotExist:
#     #     user, created = CustomUser.objects.get_or_create(email=email)
#     #     serializer = UserSerializer(user, data={
#     #     'gender': kakao_account.get("gender"),
#     #     'age_range': kakao_account.get("age_range"),
#     #     'profile_image': kakao_account["profile"].get("profile_image_url"),
#     #     'nickname': kakao_account["profile"].get("nickname"),
#     #     'kakao_oid': profile_json.get("id"),
#     #     }, partial=True)
#     #     if serializer.is_valid():
#     #         serializer.save()

#     #     data = {'access_token':access_token, 'code': code}
#     #     accept = requests.post(f"http://127.0.0.1:8000/accounts/kakao/login/finish/", data =data)
#     #     accept_status = accept.status_code

#     #     if accept_status != 200:
#     #         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
#     #     accept_json = accept_json()
#     #     accept_json.pop('user',None)
#     #     return JsonResponse(accept_json)

#     user, created = CustomUser.objects.get_or_create(email=email)

#     serializer = UserSerializer(user, data={
#         'gender': kakao_account.get("gender"),
#         'age_range': kakao_account.get("age_range"),
#         'profile_image': kakao_account["profile"].get("profile_image_url"),
#         'nickname': kakao_account["profile"].get("nickname"),
#         'kakao_oid': profile_json.get("id"),
#     }, partial=True)

#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse({"message": "Login success", "access_token": access_token}, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함
    
def kakao_callback(request):
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

def profile(request):
    access_token = request.user.access_token 
    return Response({"access_token":access_token})