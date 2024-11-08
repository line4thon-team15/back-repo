from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, ReviewLike
from .serializers import ReviewSerializer, ReviewLikeSerializer
from django.db.models import F

class ReviewsAPIView(APIView):
    def get(self, request, service_id=None):
        if service_id:
            reviews = Review.objects.filter(service_id=service_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_id):
        serializer = ReviewSerializer(
            data=request.data,
            context={
                'request': request,
                'service_id': service_id
                })
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewAPIView(APIView):
    def get(self, request, pk):
        review = Review.objects.get(id=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        review = Review.objects.get(id=pk)
        serializer = ReviewSerializer(review, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewLikeAPIView(APIView):
    def post(self, request, pk):
        review = Review.objects.get(id=pk)
        user = request.user
        like, created = ReviewLike.objects.get_or_create(review=review, user=user)

        if not created:
            like.delete()
            review.likes_count = F('likes_count') - 1
            liked = False
        else:
            review.likes_count = F('likes_count') + 1
            liked = True

        review.save()
        review.refresh_from_db()

        serializer = ReviewLikeSerializer({
            'liked': liked,
            'likes_count': review.likes_count
        })
        return Response(serializer.data, status=status.HTTP_200_OK)