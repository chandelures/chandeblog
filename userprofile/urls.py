from django.urls import path, re_path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

"""定义url模式"""
app_name = 'userprofile'

urlpatterns = [
    # 个人信息
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
