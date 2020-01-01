from django.views.generic.edit import UpdateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from userprofile.models import User


class ProfileView(UpdateView):
    """用户个人资料页面"""
    model = User
    template_name = 'account/profile.html'
    fields = ['username', 'email', 'link', 'resume', ]

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = request.user
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = request.user
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AjaxAvatarChangeView(View):
    """更改用户头像"""

    @method_decorator(login_required)
    def post(self, request):
        if request.is_ajax():
            avatar_file = request.FILES['avatar']
            user = request.user
            user.avatar.delete(save=False)
            user.avatar = avatar_file
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})
