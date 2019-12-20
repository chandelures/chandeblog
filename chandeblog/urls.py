"""chandeblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import settings

urlpatterns = [

    # 后台管理页面
    path('admin/', admin.site.urls),

    # 博客页面
    path('', include('blog.urls', namespace='blog')),

    # 用户页面
    path('accounts/', include('userprofile.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # mdeditor
    path('mdeditor/', include('mdeditor.urls')),

    # favicon
    path('favicon.ico', RedirectView.as_view(url=r'static/img/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
