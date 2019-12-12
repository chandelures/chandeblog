from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TodayArchiveView, YearArchiveView, MonthArchiveView, \
    DayArchiveView
from django.db.models import F
from .models import Post, Category


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
