from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny

from .models import Service, PresentationImage, Member
from .serializers import ServiceSerializer, ServicePresentationSerializer, ServiceMemberSerializer, ServiceListSerializer

# Create your views here.

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('team')
    serializer_class = ServiceSerializer
    # 나중에 권한 변경
    permission_classes = [AllowAny]

# 나중에 개별 이미지 수정 확인
# class PresentationImageViewSet(viewsets.ModelViewSet):
#     queryset = PresentationImage.objects.all()
#     serializer_class = ServicePresentationSerializer

#     def destroy(self, request, *args, **kwargs):
#         """개별 이미지 삭제를 위한 destroy 메서드 오버라이드"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

class MemberViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
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