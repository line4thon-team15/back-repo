from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate, logout
from users.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken



import json


# Create your views here.
User = get_user_model()

def load_participants():
    with open('users/participants.json','r', encoding='utf-8') as f:
        return json.load(f)

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        is_participant= request.data.get('is_participant')
        name = request.data.get('name')
        univ = request.data.get('univ')
        team = request.data.get('team')

        #아이디 유효성 검사
        if (User.objects.filter(username=username)).exists():
            return Response({"error":"이미 존재하는 아이디입니다."}, status = status.HTTP_400_BAD_REQUEST)

        #비밀번호 일치 및 유효성 검사
        if password != password2:
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        #유효한 해커톤 참가자 정보인지 검사
        participants = load_participants()
        if is_participant:
            team_data = participants.get(str(team))

            if not any(p['name'] == name and p['univ'] == univ for p in team_data):
                return Response({"error": "참가자 정보가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

        #직렬화기를 이용한 마지막 유효성 검사 및 사용자 생성
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"회원가입에 성공하셨습니다!!!"},status=status.HTTP_201_CREATED)
        
#로그인
class LoginView(APIView):
    permission_classes = [AllowAny]    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        #사용자 인증
        user = authenticate(request, username=username, password = password)
        #토큰 발급
        if user:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            return Response({
                'access' : str(access_token),
                'refresh': str(refresh_token),
                'username': user.username
            })
        
        #로그인 실패 => 유효하지 않은 사용자 정보
        else:
                return Response({'error':'ⓘ 아이디와 비밀번호를 정확히 입력해주세요.'},status=401)

        
#로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({'detail:':'refreshtoken이 필요합니다'},status = status.HTTP_400_BAD_REQUEST)
        
        try:
             # logout 성공시 RefreshToken 객체를 blacklist에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()

            #유효하지 않은 token outstandingtoken에서 제거
            OutstandingToken.objects.filter(token=token).delete()
            return Response({'success':'로그아웃 성공!!!'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#access token이 만료되었을 경우 refresh token을 발급해줄 클래스 설정
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)

        #refresh token의 유효성 검사
        try:
            serializer.is_valid(raise_exception=True)

        #재로그인이 필요한 시점     
        except Exception as e:
            return Response({'detail': '리프레시 토큰이 유효하지 않거나 만료되었습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        # 유효한 refresh token으로부터 새로운 액세스 토큰 생성
        new_access_token = serializer.validated_data['access']

        
        return Response({'access': new_access_token}, status=status.HTTP_200_OK)        
