from django.urls import path

from userprofile import views

app_name = 'userprofile'

urlpatterns = [
    path('profile', views.ProfileDetail.as_view(), name="profile"),
]
