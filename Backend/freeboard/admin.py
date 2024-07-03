from django.contrib import admin
from .models import FreeboardPost, FreeboardPostComment

# Register your models here.
admin.site.register(FreeboardPost)
admin.site.register(FreeboardPostComment)