from django.contrib import admin
from .models import Review, Place, WomenOnlyPlace

# Register your models here.
admin.site.register(Review)
admin.site.register(Place)
admin.site.register(WomenOnlyPlace)