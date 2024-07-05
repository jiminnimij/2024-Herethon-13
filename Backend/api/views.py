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
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from shesplace.settings import SECRET_KEY
import logging
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8000/"
KAKAO_CALLBACK_URI = BASE_URL + "accounts/kakao/login"

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthAPIView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
    	# 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email,gender")

def kakao_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    data = {'grant_type': "authorization_code", 'client_id': client_id,
            'redirect_uri': KAKAO_CALLBACK_URI,
            'code': code}
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    token_response = requests.post('https://kauth.kakao.com/oauth/token', data = data, headers = headers)
    access_token = token_response.json().get('access_token')

    headers = {"Authorization": f'Bearer {access_token}'}
    token_validate_response = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers = headers)
    print(token_validate_response.json())

    headers = {"Authorization": f'Bearer {access_token}', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    user_info_response = requests.post('https://kapi.kakao.com/v2/user/me', headers = headers)
    print(user_info_response.json())
    # code로 access token 요청

    token_response_json = token_response.json()

    # 에러 발생 시 중단
    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")
    #여기 post를 get으로 수정
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    # return JsonResponse({"profile_json":profile_json})
    kakao_oid = profile_json['id']
    nickname = profile_json['kakao_account']['profile']
    email = profile_json['kakao_account']['email']
    gender = profile_json['kakao_account']['gender']
    age_range = profile_json['kakao_account']['age_range'] 
    profile_image = profile_json['kakao_account']['profile']['profile_image_url']


    
    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUser.object.get(email=email)
        social_user = SocialAccount.objects.get(user=user)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}api/user/google/login/finish/", data=data)
        accept_status = accept.status_code  

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except CustomUser.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        
        user_data = {
            "email" : email,
            "kakao_oid" : kakao_oid,
            "gender" : gender,
            "age_range" : age_range,
            "profile_image" : profile_image,
            "nickname" : nickname
        }
        print(user_data)
        user = CustomUser.objects.create(
            email=email,
            defaults={
                "nickname":f"{nickname}",
                "kakao_oid":kakao_oid,
                "profile_image":f"{profile_image}",
                "age_range":f"{age_range}",
                "gender":f"{gender}"
            }
        )


        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}api/user/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


class Profile(ModelViewSet):

    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user  # Get the logged-in usere
        return CustomUser.objects.filter(email=user.email)
    
    # @action(detail=False, methods=['patch'], url_path='update-nickname')
    # def update_nickname(self, request, *args, **kwargs):
    #     user = self.get_queryset().first()  # Get the first user object filtered by email
    #     new_nickname = request.data.get('nickname')  # Assuming 'nickname' is in request data

    #     if new_nickname:
    #         user.nickname = new_nickname
    #         user.save()
    #         serializer = self.get_serializer(user)
    #         return Response(serializer.data)
    #     else:
    #         return Response({'error': 'Nickname field is required'}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, *args, **kwargs):
    #     user = self.request.user
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)
