from rest_framework import serializers
from .models import Review, ReviewLike

class ReviewSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    ui_tags = serializers.SerializerMethodField()
    completion_tags = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('writer', 'likes_count', 'created_at', 'updated_at', 'is_liked', 'is_writer')
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        # 태그 유효성 검사 
        review = Review.objects.create(**validated_data)
        review.tags = tags
        review.save()
        return review

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        # 태그 유효성 검사 
        review = super().update(instance, validated_data)
        review.tags = tags
        review.save()
        return review

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
    
    def get_ui_convenience_tags(self, obj):
        return obj.ui_tags

    def get_originality_completion_tags(self, obj):
        return obj.completion_tags

class ReviewLikeSerializer(serializers.Serializer):
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()