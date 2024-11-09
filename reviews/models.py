from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from services.models import Service

def get_service_for_team(team_id):
    try:
        return Service.objects.get(team=team_id)
    except Service.DoesNotExist:
        return None

class Review(models.Model):
    UI_TAGS = [
        ('EASY', '원하는 기능을 쉽게 찾을 수 있어요'),
        ('SIMPLE', '사용 방법이 간편해요'),
        ('ERROR_FREE', '오류 해결이 쉬워요'),
        ('DESIGN', '디자인이 예뻐요'),
        ('GROWTH', '가시성이 좋아요'),
        ('FEEDBACK', '피드백이 명확해요'),
    ]
    
    COMPLETION_TAGS = [
        ('BASIC', '서비스가 기본해요'),
        ('REUSE', '다시 이용하고 싶어요'),
        ('LOADING', '로딩이 빨라요'),
        ('ORIGINAL', '원하는 기능이 있어요'),
    ]

    ALL_TAGS = UI_TAGS + COMPLETION_TAGS

    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                related_name='reviews')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE,
                                null=True, blank=True, related_name='reviews')
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)
        ])
    tags = models.JSONField(default=list)
    review = models.TextField()
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [ # 서비스당 리뷰 1개
            models.UniqueConstraint(fields=['writer', 'service'],
                                    name='unique_review_per_team')
        ]

    def clean(self):
        super().clean()

        # 태그 유효성
        if not isinstance(self.tags, list):
            raise ValidationError({
                'tags': '태그는 리스트 형태여야 합니다.'
            })
        
        # 태그 개수
        if len(self.tags) > 5:
            raise ValidationError({
                'tags': '태그는 최대 5개 선택할 수 있습니다.'
            })
        
        # 태그 유효성
        valid_tags = {tag[0] for tag in self.ALL_TAGS}
        for tag in self.tags:
            if tag not in valid_tags:
                raise ValidationError({
                    'tags': f'"{tag}"는 유효하지 않은 태그입니다.'
                })
        

    def save(self, *args, **kwargs):
        if not self.service:
            self.service = get_service_for_team(self.team)
        else:
            self.team = self.service.team
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def ui_tags(self): # UI 태그 반환
        valid_tags = {tag[0] for tag in self.UI_TAGS}
        return [tag for tag in self.tags if tag in valid_tags]

    @property
    def completion_tags(self): # 완성도 태그 반환
        valid_tags = {tag[0] for tag in self.COMPLETION_TAGS}
        return [tag for tag in self.tags if tag in valid_tags]


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [ # 리뷰당 좋아요 1개
            models.UniqueConstraint(fields=['review', 'user'], name='unique_review_like')
        ]