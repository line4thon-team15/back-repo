from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from .models import Service, PresentationImage, Member
from .serializers import ServiceSerializer, ServicePresentationSerializer, ServiceMemberSerializer, ServiceListSerializer

from rest_framework.response import Response

import pandas as pd
import json
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('team')
    serializer_class = ServiceSerializer
    # permission_classes = [AllowAny]
    def get_permissions(self):
        if self.action in ["update", "delete", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        elif self.action == "destroy":
            return [IsAdminUser()]
        else:
            return [AllowAny()]

# 나중에 개별 이미지 수정 확인
# class PresentationImageViewSet(viewsets.ModelViewSet):
#     queryset = PresentationImage.objects.all()
#     serializer_class = ServicePresentationSerializer

#     def destroy(self, request, *args, **kwargs):
#         """개별 이미지 삭제를 위한 destroy 메서드 오버라이드"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

class MemberViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Member.objects.all()
    serializer_class = ServiceMemberSerializer
    permission_classes = [AllowAny]

class PresentationViewSet(viewsets.ModelViewSet):
    queryset = PresentationImage.objects.all()
    serializer_class = ServicePresentationSerializer
    permission_classes = [AllowAny]

#전체 서비스 목록 불러오기
class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    permission_classes=[AllowAny]

class TeamDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # CSV 파일 업로드 확인
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "파일이 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # CSV 파일을 DataFrame으로 로드
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({"error": f"파일을 읽을 수 없습니다: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # 팀별 데이터 정리
        team_data = {}
        for team, group in df.groupby("팀"):
            team_data[team] = [
                {"이름": row["이름"], "파트": row["파트"]} 
                for index, row in group.iterrows()
            ]
        
        # JSON 파일로 저장
        json_file_path = 'services/members.json'  # 실제 저장 경로에 맞게 수정
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(team_data, json_file, ensure_ascii=False, indent=4)

        Service.objects.all().delete()  # 모든 서비스 삭제
        Member.objects.all().delete()   # 모든 멤버 삭제

        for team_id, members in team_data.items():
            team_number = int(team_id)  # 팀 번호를 int로 변환

            # 서비스가 존재하는지 확인하고, 없으면 생성
            service_instance, created = Service.objects.get_or_create(team=team_number)

            # 멤버 생성
            for member in members:
                member_name = member["이름"]
                member_part = member["파트"]
                Member.objects.create(service=service_instance, member=member_name, part=member_part)

        return Response(team_data, status=status.HTTP_200_OK)