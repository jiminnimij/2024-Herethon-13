from django.db import models

# Create your models here.

# 채용게시판 게시글 모델
class RecruitboardPost(models.Model):
    recruit_post_location = models.TextField(verbose_name='채용을 진행하는 곳의 위치')
    recruit_post_title = models.TextField(verbose_name='게시글 제목')
    recruit_post_content = models.TextField(verbose_name='게시글 내용')
    free_post_created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    recruit_post_company = models.TextField(verbose_name='채용 진행 회사명')
    recruit_post_img  = models.ImageField(verbose_name='게시글 대표 이미지')
