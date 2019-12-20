from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import generic
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.formats import date_format

from blog.models import Post, Category, Column


class IndexView(generic.ListView):
    """主页"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().public()


def ajax_post_list(request):
    if request.is_ajax():
        index = int(request.GET.get("index", 0))
        count = int(request.GET.get("count", 0))
        post_count = Post.objects.count()
        data = []
        for i in range(count):
            if 0 <= index < post_count:
                post = Post.objects.all()[index]
                index = index + 1
                data.append({
                    "post_count": post_count,
                    "post_title": post.title,
                    "post_abstract": post.abstract[:100] + "......",
                    "post_category_name": post.category.name,
                    "post_create_date": date_format(post.create_date, format="Y.m.j"),
                })
            else:
                return JsonResponse(data, safe=False)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status": "error"})


def ajax_post_count(request):
    if request.is_ajax():
        post_count = Post.objects.count()
        data = {
            "post_count": post_count,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"status": "error"})


class PostView(generic.DetailView):
    """文章详细页面"""
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().public()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Post.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        return response


class PostCreate(generic.CreateView):
    """文章创建页面"""
    model = Post
    template_name = 'blog/create.html'


class PostUpdate(generic.UpdateView):
    """文章更新页面"""
    model = Post
    template_name = 'blog/post_update.html'


class PostDelete(generic.DeleteView):
    """文章删除页面"""
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name_suffix = 'blog/post_check_delete.html'


class PostTodayArchive(generic.TodayArchiveView):
    """归档页面"""
    allow_empty = True
    allow_future = False
    context_object_name = 'post_list'
    template_name = 'blog/archive.html'
    http_method_names = [u'get', ]
    model = Post
    date_field = 'create_date'
    paginate_by = 50
    make_object_list = True


class PostYearArchive(generic.YearArchiveView):
    """文章归档页面"""
    allow_empty = True
    allow_future = False
    context_object_name = 'post_list'
    template_name = 'blog/archive.html'
    http_method_names = [u'get', ]
    model = Post
    date_field = 'create_date'
    year_format = '%Y'
    paginate_by = 50
    make_object_list = True


class PostMonthArchive(generic.MonthArchiveView):
    """文章归档页面"""
    allow_empty = True
    allow_future = False
    context_object_name = 'post_list'
    template_name = 'blog/archive.html'
    http_method_names = [u'get', ]
    model = Post
    date_field = 'create_date'
    year_format = '%Y'
    month_format = '%m'
    paginate_by = 50
    make_object_list = True


class PostDayArchive(generic.DayArchiveView):
    """文章归档页面"""
    allow_empty = True
    allow_future = False
    context_object_name = 'post_list'
    template_name = 'blog/archive.html'
    http_method_names = [u'get', ]
    model = Post
    date_field = 'create_date'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    paginate_by = 50
    make_object_list = True
