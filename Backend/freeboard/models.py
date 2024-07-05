from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# User = get_user_model()
from api.models import CustomUser

# 자유게시판 게시글 모델
class FreeboardPost(models.Model):
    free_post_location = models.TextField(verbose_name='게시글 작성 위치')
    free_post_title = models.TextField(verbose_name='게시글 제목')
    free_post_content = models.TextField(verbose_name='게시글 내용')
    free_post_created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    # 기본 User 참조. 후에 커스텀 User로 변경 필요
    free_post_writer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name='글작성자', null=True, blank=True)

# 자유게시판 댓글 모델
class FreeboardPostComment(models.Model):
    free_comment_content = models.TextField(verbose_name='댓글 내용')
    free_comment_created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    free_comment_post_id = models.ForeignKey(to=FreeboardPost, on_delete=models.CASCADE, db_column="post_id")
    # 기본 User 참조. 후에 커스텀 User로 변경 필요
    free_comment_writer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name='댓글작성자', null=True, blank=True)
