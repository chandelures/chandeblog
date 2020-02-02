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
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from blog.models import Post
from . import settings

sitemaps = {
    'blog': GenericSitemap({'queryset': Post.objects.all(), 'date_field': 'create_date'}, priority=0.6),
}
urlpatterns = [
    # 后台管理页面
    path('admin/', admin.site.urls),

    # 博客页面
    path('', include('blog.urls', namespace='blog')),

    # 评论页面
    path('comment/', include('comment.urls', namespace='comment')),

    # 消息通知
    # path('inbox/notifications/', include('notifications.urls', namespace='notifications')),

    # 用户页面
    path('accounts/', include('userprofile.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # mdeditor
    path('mdeditor/', include('mdeditor.urls')),

    # search
    path('search/', include('haystack.urls')),

    # api
    path('api/', include('api.urls', namespace='api')),

    # favicon
    path('favicon.ico', RedirectView.as_view(url=r'static/img/favicon.ico')),

    # sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
