from django.shortcuts import render
from django.views.generic import FormView, UpdateView, DeleteView, DetailView

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from userprofile.forms import UserLoginForm
from userprofile.models import Profile


class ProfileView(DetailView):
    """用户个人资料页面"""
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
