import json
from django.db.models import Avg
from django.db.models import Case, When
from rest_framework import serializers
from .models import Service, PresentationImage, Member
from reviews.serializers import ReviewSerializer

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
        read_only_fields = ['id', 'member']

    def create(self, validated_data):
        # 새로운 Member 객체 생성
        return Member.objects.create(**validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    presentations = serializers.SerializerMethodField()
    presentation_cnt = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    review_cnt = serializers.SerializerMethodField()
    score_average = serializers.SerializerMethodField()
    service_member = serializers.SerializerMethodField()

    def get_presentations(self, obj):
        image = obj.image.all()
        return ServicePresentationSerializer(instance=image, many=True, context=self.context).data
    
    def get_presentation_cnt(self, obj):
        return obj.image.count()
    
    def get_members(self, obj):
        part_order = {'PM/PD': 0, 'FE': 1, 'BE': 2}

        # members 정렬: part 우선, 그 다음 member의 ㄱㄴㄷ 순서
        members = obj.member.filter(part__isnull=False).order_by(
            Case(
                *(When(part=key, then=val) for key, val in part_order.items())
            ),
            'member'  # 한글 이름은 기본적으로 ㄱㄴㄷ 순으로 정렬
        )
        return ServiceMemberSerializer(members, many=True).data

    def get_review(self, obj):
        request = self.context['request']
        serializer = ReviewSerializer(obj.reviews, many=True, context={'request': request})
        return serializer.data
    
    def get_review_cnt(self, obj):
        return obj.reviews.count()
    
    def get_score_average(self, obj):
        score_avg = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return round(score_avg, 2) if score_avg is not None else 0.0
    
    def get_service_member(self, obj):
        team = obj.team
        member = self.context['request'].user
        # Check if the user is authenticated before accessing `team`
        if member.is_authenticated:
            return member.team == team
        else:
            return False
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

        return instance

    def update(self, instance, validated_data):
        if 'thumbnail_image' not in validated_data:
            validated_data['thumbnail_image'] = instance.thumbnail_image

        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.team = validated_data.get('team', instance.team)
        instance.content = validated_data.get('content', instance.content)
        instance.site_url = validated_data.get('site_url', instance.site_url)
        instance.thumbnail_image = validated_data.get('thumbnail_image', instance.thumbnail_image)
        instance.intro = validated_data.get('intro', instance.intro)
        instance.save()

        new_images = self.context['request'].FILES.getlist('image')
        if new_images:
            instance.image.all().delete()
    
            # 새 이미지 추가
            for image_data in new_images:
                PresentationImage.objects.create(service=instance, image=image_data)

        # 멤버 데이터 업데이트 또는 추가
        members_data = self.context['request'].data.get('members', [])
        for member_data in members_data:
            member_id = member_data.get('id')
            part = member_data.get('part')
            
            if member_id:
                # 기존 멤버 업데이트
                member = instance.member.filter(id=member_id).first()
                if member:
                    member.part = part
                    member.save()
            else:
                # id가 없는 경우 새로운 멤버 생성
                Member.objects.create(service=instance, member=member_data['member'], part=part)
        return instance
    

class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'team', 'thumbnail_image']
