from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView

"""定义url模式"""
app_name = 'userprofile'

urlpatterns = [

    # 个人信息
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    # 注销
    # url(r'^logout/$', LogoutView.as_view(next_page='/'), name='logout'),

]
