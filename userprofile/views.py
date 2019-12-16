from django.shortcuts import render
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, DetailView
from .forms import UserLoginForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class ProfileView(DetailView):
    """用户个人资料页面"""
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
