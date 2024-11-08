import json
from django.db.models import Case, When
from rest_framework import serializers
from .models import Service, PresentationImage, Member

class ServicePresentationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = PresentationImage
        fields = ['id','service', 'image']

class ServiceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'member', 'part']

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
        part_order = {'PM/PD': 0, 'FE': 1, 'BE': 2}

        # members 정렬: part 우선, 그 다음 member의 ㄱㄴㄷ 순서
        members = obj.member.all().order_by(
            Case(
                *(When(part=key, then=val) for key, val in part_order.items())
            ),
            'member'  # 한글 이름은 기본적으로 ㄱㄴㄷ 순으로 정렬
        )
        return ServiceMemberSerializer(members, many=True).data

    class Meta:
        model = Service
        fields = '__all__'
    
    def create(self, validated_data):
        # Create the Service instance
        instance = Service.objects.create(**validated_data)

        # Save presentation images
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PresentationImage.objects.create(service=instance, image=image_data)

        # Load team members from JSON file
        members_file_path = 'services/members.json'  # Update with the actual file path
        with open(members_file_path, 'r', encoding='utf-8') as file:
            members_data = json.load(file)

        # Retrieve members for the given team and save to DB
        team_members = members_data.get(str(instance.team), [])
        for member_name in team_members:
            Member.objects.create(service=instance, member=member_name)

        return instance

    def update(self, instance, validated_data):
        if 'thumbnail_image' not in validated_data:
            validated_data['thumbnail_image'] = instance.thumbnail_image

        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.team = validated_data.get('team', instance.team)
        instance.content = validated_data.get('content', instance.content)
        instance.site_url = validated_data.get('site_url', instance.site_url)
        instance.thumbnail_image = validated_data.get('thumbnail_image', instance.thumbnail_image)
        instance.save()

        new_images = self.context['request'].FILES.getlist('image')
        if new_images:
            instance.image.all().delete()
            for image_data in new_images:
                PresentationImage.objects.create(service=instance, image=image_data)
        
        members_file_path = 'services/members.json'  # Update with the actual file path
        with open(members_file_path, 'r', encoding='utf-8') as file:
            members_data = json.load(file)

        # Retrieve members for the given team and save to DB
        team_members = members_data.get(str(instance.team), [])
        instance.member.all().delete()
        for member_name in team_members:
            Member.objects.create(service=instance, member=member_name)
        return instance
    

'''class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'team', 'thumbnail_imgae']'''
