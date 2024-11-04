from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from users.serializers import *
from rest_framework.authtoken.models import Token
import json


# Create your views here.
User = get_user_model()

def load_participants():
    with open('users/participants.json','r', encoding='utf-8') as f:
        return json.load(f)

class SignUpView(APIView):
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
            if not any(p['name'] == name and p['univ'] == univ for p in participants[team]):
                return Response({"error": "참가자 정보가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

        #직렬화기를 이용한 마지막 유효성 검사 및 사용자 생성
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"회원가입에 성공하셨습니다!!!"},status=status.HTTP_201_CREATED)
        
#로그인
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        #사용자 인증
        user = authenticate(request, username=username, password = password)

        #토큰 발급
        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'username':user.username})
        
        #로그인 실패
        else:
                return Response({'error':'ⓘ 아이디와 비밀번호를 정확히 입력해주세요.'},status=401)

        
#로그아웃
#class LogoutView(APIView):
#    def post(self, request):
