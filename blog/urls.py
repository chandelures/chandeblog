from django.conf.urls import url
from . import views

"""定义url模式"""
app_name = 'blog'

urlpatterns = [
    # 主页
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 文章页
    url(r'^post/(?P<slug>[^\\.]+)/$', views.PostView.as_view(), name='post'),
]
