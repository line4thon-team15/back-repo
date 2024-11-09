from rest_framework import serializers
from .models import Review, ReviewLike
from services.models import Service
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError
        
class ReviewSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    ui_tags = serializers.SerializerMethodField()
    completion_tags = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    writer_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('writer', 'likes_count', 'created_at', 'updated_at', 'is_liked', 'is_writer', 'service')
    
    def get_team(self, obj):
        return obj.writer.team
    
    def get_writer_name(self, obj):
        return obj.writer.name

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        score = validated_data.pop('score')
        review_text = validated_data.pop('review')
        service_id = self.context.get('service_id')

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise ValidationError("유효하지 않은 service_id입니다.")
        
        writer = self.context['request'].user
        validated_data['writer'] = writer
        validated_data['service'] = service

        if writer.team == service.team:
            raise ValidationError("내 팀의 서비스에는 리뷰를 작성할 수 없습니다.")
        
        # 리뷰 생성
        review = Review.objects.create(score=score, tags=tags, review=review_text, **validated_data)
        return review
    
    def update(self, instance, validated_data):
        # 수정 가능한 필드만 업데이트
        instance.score = validated_data.get('score', instance.score)
        instance.review = validated_data.get('review', instance.review)
        instance.tags = validated_data.get('tags', instance.tags)
        
        instance.save()
        return instance

    def get_is_liked(self, obj): # 좋아요 눌렀는지
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReviewLike.objects.filter(
                review = obj,
                user = request.user
            ).exists()
        return False

    def get_is_writer(self, obj): # 작성자인지
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.writer == request.user
        return False
    
    def get_ui_tags(self, obj):
        return obj.ui_tags

    def get_completion_tags(self, obj):
        return obj.completion_tags

class ReviewLikeSerializer(serializers.Serializer):
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()