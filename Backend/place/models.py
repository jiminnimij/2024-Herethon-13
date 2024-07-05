from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# User = get_user_model()
from api.models import CustomUser
# Create your models here.

class Place(models.Model):
    # 장소 정보
    place_name = models.TextField(verbose_name='장소명')
    place_detail = models.TextField(verbose_name='설명')
    place_img = models.ImageField(verbose_name='대표 사진')
    place_time = models.TextField(verbose_name='운영시간')
    place_site = models.URLField(verbose_name='관련 사이트')
    place_call  = models.TextField(verbose_name='전화번호')

    # 위치 관련
    place_location = models.TextField(verbose_name='도로명 주소')
    place_lat = models.FloatField(verbose_name='위도')
    place_lon  = models.FloatField(verbose_name='경도')
    
class Review(models.Model):
    # 기본 User 참조. 후에 커스텀 User로 변경 필요
    review_writer_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='작성자', null=True, blank=True)
    review_content = models.TextField(verbose_name='리뷰 내용')
    review_place_id = models.ForeignKey(to=Place, on_delete=models.CASCADE, verbose_name='리뷰가 달린 장소 id', null=True, blank=True)
    review_rate = models.IntegerField(verbose_name='별점')

class WomenOnlyPlace(models.Model):
    place = models.ForeignKey(to=Place, on_delete=models.CASCADE, null=True, blank=True, related_name='women_only_places')

    CATEGORY_CHOICES = [
        ('BEAUTY', '뷰티'),
        ('GYM', '헬스장'),
        ('STUDY', '스터디카페/독서실'),
        ('HOSPITAL', '병원'),
        ('ACCOMMODATION', '숙박'),
        ('HOUSING', '주거'),
        ('RESTAURANT', '술집/음식점'),
        ('CENTER', '여성전용센터'),
        ('SAUNA', '사우나'),
        ('RESTROOM', '화장실'),
    ]

    women_only_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)

class Scrap(models.Model):
    scrap_place = models.ForeignKey(to=Place, on_delete=models.CASCADE, null=True, blank=True, related_name='scrap_place')
    scrap_user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name='스크랩한 유저', null=True, blank=True)

