from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

# 자유게시판 게시글 모델
class FreeboardPost(models.Model):
    free_post_location = models.TextField(verbose_name='게시글 작성 위치')
    free_post_title = models.TextField(verbose_name='게시글 제목')
    free_post_content = models.TextField(verbose_name='게시글 내용')
    free_post_created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    # 기본 User 참조. 후에 커스텀 User로 변경 필요
    free_post_writer_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='작성자', null=True, blank=True)

