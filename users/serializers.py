from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from services.serializers import ServiceSerializer
from reviews.models import Review
from services.models import *

User = get_user_model()

class UserSerializer(ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password','password2', 'is_participant','name','univ', 'team', 'techrole')
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ServiceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'thumbnail_image']

class ProfileSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    service_cnt = serializers.SerializerMethodField()

    def get_service(self, obj):
        reviews = Review.objects.filter(writer=obj)
        services = [review.service for review in reviews if review.service]

        return ServiceSummarySerializer(services, many=True).data
    
    def get_service_cnt(self, obj):
        return Review.objects.filter(writer=obj, service__isnull=False).count()

    class Meta:
        model = User
        fields = ['name', 'is_participant', 'univ', 'team', 'service', 'profile_pic', 'service_cnt']
        read_only_fields = ['name', 'is_participatn', 'univ', 'team', 'service', 'service_cnt']
    
