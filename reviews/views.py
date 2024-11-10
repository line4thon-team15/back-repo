from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, ReviewLike
from .serializers import ReviewSerializer, ReviewLikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

class IsReviewWriter(permissions.BasePermission):
    message = "리뷰 작성자가 아닙니다."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.writer == request.user

class CanLikeReview(permissions.BasePermission):
    message = "본인에 리뷰에 좋아요를 할 수 없습니다."

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.writer != request.user

class ReviewsAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsReviewWriter()]
        return [IsAuthenticated()]
    
    def get(self, request, service_id=None, review_id=None):
        if review_id:
            try:
                review = Review.objects.get(id=review_id, service_id=service_id)
                serializer = ReviewSerializer(instance=review, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Review.DoesNotExist:
                raise ValidationError("해당 리뷰를 찾을 수 없습니다.")

        if service_id:
            reviews = Review.objects.filter(service_id=service_id)
        else:
            reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
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
    
    def put(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
            self.check_object_permissions(request, review)
            
            serializer = ReviewSerializer(
                review,
                data=request.data,
                context={'request': request},
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Review.DoesNotExist:
            raise ValidationError("해당 리뷰를 찾을 수 없습니다.")

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review)
            
            review.delete()
            return Response(
                {"message": "리뷰가 삭제되었습니다."}, 
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Review.DoesNotExist:
            raise ValidationError("해당 리뷰를 찾을 수 없습니다.")

class ReviewLikeAPIView(APIView):
    permission_classes = [IsAuthenticated, CanLikeReview]

    def post(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
            self.check_object_permissions(request, review)

            user = request.user
            like, created = ReviewLike.objects.get_or_create(review=review, user=user)

            if not created:
                like.delete()
                review.likes_count -= 1
                liked = False
            else:
                review.likes_count += 1
                liked = True

            review.save()
            review.refresh_from_db()

            serializer = ReviewLikeSerializer({
                'liked': liked,
                'likes_count': review.likes_count
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Review.DoesNotExist:
            raise ValidationError("해당 리뷰를 찾을 수 없습니다.")