from django.shortcuts import render
from rest_framework import viewsets, mixins

from .models import Service, PresentationImage
from .serializers import ServiceSerializer, ServicePresentationSerializer

# Create your views here.

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('team')
    serializer_class = ServiceSerializer

# 나중에 개별 이미지 수정 확인
# class PresentationImageViewSet(viewsets.ModelViewSet):
#     queryset = PresentationImage.objects.all()
#     serializer_class = ServicePresentationSerializer

#     def destroy(self, request, *args, **kwargs):
#         """개별 이미지 삭제를 위한 destroy 메서드 오버라이드"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)