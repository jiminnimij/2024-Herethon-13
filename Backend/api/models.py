import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일 필드가 작성되어야 합니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    kakao_oid = models.BigIntegerField(
        null=True, unique=True, blank=False
    )  # 카카오 user_id
    
    gender = models.CharField(max_length=100)
    age_range = models.CharField(max_length=100, null=True, blank=True)
    # position = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.URLField(max_length=200, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMO6VQCqNMCRlC6jtWeS8xDW9LwyFhhjuiCQ&s", null=True)
    defaultname = "USER"

# 랜덤 넘버 생성 (예: 1부터 100 사이의 랜덤 정수)
    random_number = random.randint(1, 100)

# 기본 이름에 랜덤 넘버 추가
    defaultname_with_random = f"{defaultname}{random_number}" 
    nickname = models.CharField(max_length=100, unique=False, null=True, default=defaultname_with_random)
    
    is_staff = models.BooleanField(default=False)  # 슈퍼유저 권한
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # 계정 활성화 상태
    created_at = models.DateTimeField(auto_now_add=True)

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email