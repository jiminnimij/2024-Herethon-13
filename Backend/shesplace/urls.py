"""
URL configuration for shesplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('freeboard/', include('freeboard.urls')),
<<<<<<< HEAD
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/kakao/', include('api.urls')),
=======
    path('recruitboard/', include('recruitboard.urls'))
>>>>>>> b3ed7cb9d7611952cca92e11be84824aea10156f
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
