from django.shortcuts import render
from django.views.generic import FormView, UpdateView, DeleteView, DetailView

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from userprofile.models import User


class ProfileView(DetailView):
    """用户个人资料页面"""
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
