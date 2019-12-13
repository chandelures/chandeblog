from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TodayArchiveView, YearArchiveView, MonthArchiveView, \
    DayArchiveView, UpdateView, CreateView, DeleteView
from django.db.models import F
from django.urls import reverse_lazy
from .models import Post, Category, Column


class IndexView(ListView):
    """主页"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().public()


class PostView(DetailView):
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


class PostCreate(CreateView):
    model = Post
    template_name = 'blog/create.html'


class PostUpdate(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name_suffix = 'blog/post_check_delete.html'


class PostTodayArchive(TodayArchiveView):
    allow_empty = True
    allow_future = False
    context_object_name = 'post_list'
    template_name = 'blog/archive.html'
    http_method_names = [u'get', ]
    model = Post
    date_field = 'create_date'
    paginate_by = 50
    make_object_list = True


class PostYearArchive(YearArchiveView):
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


class PostMonthArchive(MonthArchiveView):
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


class PostDayArchive(DayArchiveView):
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
