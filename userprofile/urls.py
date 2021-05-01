from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from userprofile import views

app_name = 'userprofile'

urlpatterns = [
    path('users/profile', views.UserProfileDetail.as_view(), name="profile"),
    path('users', views.UserProfileList.as_view(), name='list'),

    path("token/login", obtain_auth_token, name='login'),
    path('token/logout', views.Logout.as_view(), name='logout'),
]
