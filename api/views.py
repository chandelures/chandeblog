from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.formats import date_format
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import markdown

from blog.models import Post
from haystack.forms import ModelSearchForm


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


class SearchRepositoriesView(View):
    def get(self, request):
        max_result = 4
        data = {
            'success': False,
        }
        if request.is_ajax():
            q = request.GET.get('q')
            if q:
                form = ModelSearchForm(request.GET)
                if form.is_valid():
                    results = form.search()
                    results_count = len(results.all())
                    data['success'] = True
                    data.update({
                        'results': {
                            'category1': {
                                'name': '文章',
                                'results': []
                            }
                        },
                        'action': {
                            "url": '/search/?q=' + q,
                            "text": '没有搜索到有关于 ' + q + ' 的内容',
                        },
                    })
                    if results.all():
                        for item in results.all()[:max_result]:
                            data.get('results').get("category1").get('results').append({
                                "title": item.object.title,
                                "url": item.object.get_absolute_url(),
                                "description": item.object.category.name,
                            })
                        data.get('action')["text"] = '查看共 ' + str(results_count) + ' 个搜索结果'
        return JsonResponse(data)
