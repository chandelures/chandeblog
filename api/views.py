from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.formats import date_format
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import markdown

from blog.models import Post


class AjaxPostListView(View):
    """获取文章列表API"""

    def get(self, request):
        if request.is_ajax():
            index = int(request.GET.get("index", 0))
            count = int(request.GET.get("count", 0))
            post_count = Post.objects.public().count()
            data = {"success": True, "post_count": post_count, "result": []}
            for i in range(count):
                if 0 <= index < post_count:
                    post = Post.objects.public()[index]
                    index = index + 1
                    data['result'].append({
                        "post_title": post.title,
                        "post_abstract": self.markdown_text(post.abstract),
                        "post_category_name": post.category.name,
                        "post_create_date": date_format(post.create_date, format="Y-m-j"),
                        "post_views": post.views,
                        "post_url": post.get_absolute_url(),
                    })
                else:
                    return JsonResponse(data, safe=False)
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"success": False})

    @staticmethod
    def markdown_text(text):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
        ])
        html = md.convert(text)
        return html


class AjaxAvatarChangeView(View):
    """更改用户头像"""

    @method_decorator(login_required)
    def post(self, request):
        if request.is_ajax():
            avatar_file = request.FILES['avatar']
            user = request.user
            if user.avatar.name != 'avatar/default.png':
                user.avatar.delete(save=False)
            user.avatar = avatar_file
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
