from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from userprofile.forms import ProfileForm
from userprofile.models import User


class ProfileView(generic.DetailView):
    """用户个人资料页面"""
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AjaxAvatarChange(generic.View):
    """更改用户头像"""

    def post(self, request):
        if request.is_ajax():
            avatar_file = request.FILES['avatar']
            user = request.user
            user.avatar = avatar_file
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})

    def get(self, request):
        form = ProfileForm()
        context = {'form': form}
        template_name = 'account/avatar_change.html'
        return render(request, template_name, context=context)
