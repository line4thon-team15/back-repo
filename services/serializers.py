import json
from rest_framework import serializers
from .models import Service, PresentationImage, Member



class ServicePresentationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PresentationImage
        fields = ['id','image']

class ServiceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['member', 'part']

    def create(self, validated_data):
        # 새로운 Member 객체 생성
        return Member.objects.create(**validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    presentations = serializers.SerializerMethodField()
    presentation_cnt = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_presentations(self, obj):
        image = obj.image.all()
        return ServicePresentationSerializer(instance=image, many=True, context=self.context).data
    
    def get_presentation_cnt(self, obj):
        return obj.image.count()
    
    def get_members(self, obj):
        # members.json 파일 경로
        members_file_path = 'services/members.json'  # 실제 경로로 변경
        
        # JSON 파일 읽기
        with open(members_file_path, 'r', encoding='utf-8') as file:
            members_data = json.load(file)

        # 팀 번호에 해당하는 멤버 리스트 가져오기
        team_members = members_data.get(str(obj.team), [])

        # 멤버 정보 직렬화 (JSON에서 직접 가져오기)
        members_info = [{'member': member_name} for member_name in team_members]

        return ServiceMemberSerializer(members_info, many=True).data

    # def get_team_members(self, obj):
    #     member = obj.team_members.members
    #     return member

    class Meta:
        model = Service
        fields = '__all__'
    
    def create(self, validated_data):
        instance = Service.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PresentationImage.objects.create(service=instance, image=image_data)
        return instance
    
    def update(self, instance, validated_data):
        # `thumbnail_image`가 업데이트 요청에 포함되지 않으면 기존 값을 유지
        # 무슨 코드를 쓸까... 프론트랑 얘기해봐야할 듯...
        # if 'thumbnail_image' not in validated_data or validated_data.get('thumbnail_image') is None:
        if 'thumbnail_image' not in validated_data:
            validated_data['thumbnail_image'] = instance.thumbnail_image

        instance.service_name = validated_data.get('service_name', instance.service_name)
        current_team = instance.team
        new_team = validated_data.get('team', current_team)
        if new_team != current_team:
            instance.team = new_team
        instance.content = validated_data.get('content', instance.content)
        instance.site_url = validated_data.get('site_url', instance.site_url)
        instance.thumbnail_image = validated_data.get('thumbnail_image', instance.thumbnail_image)
        instance.save()

        new_images = self.context['request'].FILES.getlist('image')
        if new_images:
            instance.image.all().delete()
            for image_data in new_images:
                PresentationImage.objects.create(service=instance, image=image_data)
        return instance