import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from services.models import Service
from services.serializers import ServiceSerializer

class MainRouteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        services = Service.objects.all().order_by('team')  # 팀 순서대로 전달

        data = []
        for service in services:
            service_data = {
                'id': service.id,
                'service_name': service.service_name,
                'thumbnail_image': request.build_absolute_uri(service.thumbnail_image.url) if service.thumbnail_image else None,
                'intro': service.intro,
                'team_num': service.team,
            }
            data.append(service_data)

        return Response(data)

class MainScoreView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        
        score_top5_services = sorted(serializer.data, key=lambda x: x['score_average'], reverse=True)[:5]

        data = []
        for service in score_top5_services:
            thumbnail_url = service['thumbnail_image']
            absolute_thumbnail_url = request.build_absolute_uri(thumbnail_url) if thumbnail_url else None

            service_data = {
                'id': service['id'],
                'service_name': service['service_name'],
                'thumbnail_image': absolute_thumbnail_url,
                'intro': service['content'],
                'team_num': service['team'],
                'score_average': service['score_average'],
            }
            data.append(service_data)

        # 1등 서비스에는 winner_score 추가
        if data:
            data[0]['winner_score'] = 1

        return Response(data)

class MainTagView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        service_tag_count = []

        # 서비스별 리뷰 태그 개수 계산
        for service in services:
            tag_count = 0
            # 전체 리뷰 태그 계수 계산
            for review in service.reviews.all():
                tag_count += len(review.tags)

            service_tag_count.append((service, tag_count))

        # 태그 개수 기준 정렬
        sorted_services = sorted(service_tag_count, key=lambda x: x[1], reverse=True)[:5]

        data = []
        for service, tag_count in sorted_services:
            service_data = {
                'id': service.id,
                'service_name': service.service_name,
                'thumbnail_image': request.build_absolute_uri(service.thumbnail_image.url) if service.thumbnail_image else None,
                'intro': service.content,
                'team_num': service.team,
                'tag_count': tag_count,
            }
            data.append(service_data)

        # 1등 서비스에는 winner_score 추가
        if data:
            data[0]['winner_score'] = 1

        return Response(data)

class MainRecentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # 최신순 4개
        recent_services = Service.objects.all().order_by('-updated_at')[:4]

        data = []
        for service in recent_services:
            service_data = {
                'id': service.id,
                'service_name': service.service_name,
                'thumbnail_image': request.build_absolute_uri(service.thumbnail_image.url) if service.thumbnail_image else None,
                'intro': service.content,
                'team_num': service.team,
            }
            data.append(service_data)

        return Response(data)