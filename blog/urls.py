from django.conf.urls import url
from . import views

"""定义url模式"""
app_name = 'blog'

urlpatterns = [
    # 主页
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 文章页
    url(r'^post/(?P<slug>[^\\.]+)/$', views.PostView.as_view(), name='post'),
    # 归档页面
    url(r'^archive/$', views.PostTodayArchive.as_view(), name='archive'),
    url(r'^archive/(?P<year>\d{4})/$', views.PostYearArchive.as_view()),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$', views.PostMonthArchive.as_view()),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.PostDayArchive.as_view()),
]
