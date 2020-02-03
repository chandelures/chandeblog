from api import views
from django.conf.urls import url

"""定义url模式"""
app_name = 'api'

urlpatterns = [
    # 获取文章列表
    url('getpostlist', views.AjaxPostListView.as_view()),
    # 更改头像
    url('changeavatar', views.AjaxAvatarChangeView.as_view()),
    # 搜索信息
    url('search/repositories', views.SearchRepositoriesView.as_view())
]
