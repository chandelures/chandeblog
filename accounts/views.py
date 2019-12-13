from django.shortcuts import render
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, DetailView
from .forms import UserLoginForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

