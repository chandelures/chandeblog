from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from . import views
from .models import Post

"""定义url模式"""
app_name = 'blog'

urlpatterns = [
    # 主页
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 文章页
    url(r'^post/(?P<slug>[^\\.]+)/$', views.PostView.as_view(), name='post'),
    # 归档页面
    url(r'^archive/$',
        ArchiveIndexView.as_view(model=Post, date_field="pub_date"),
        name="post_archive"),
    url(r'^<int:year>/$', views.PostYearArchive.as_view(), name='archive_year'),
    url(r'^<int:year>/<int:month>/$',
        views.PostMonthArchive.as_view(),
        name='archive_month'),
    url(r'^<int:year>/<int:month>/<int:day>/$',
        views.PostDayArchive.as_view(), name='archive_day'),
    url(r'^today/$', views.PostTodayArchive.as_view(), name='archive_today'),
]
