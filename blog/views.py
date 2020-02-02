from django.http import JsonResponse
from django.views import generic
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.formats import date_format

from blog.models import Post
from comment.models import Comment
import markdown


class IndexView(generic.TemplateView):
    """主页"""
    template_name = 'blog/index.html'


class PostView(generic.DetailView):
    """文章详细页面"""
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().public()

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object)
        recent_post_list = Post.objects.public()[:10]
        context['recent_post_list'] = recent_post_list
        context['comments'] = comments
        return context

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


class CategoryView(generic.ListView):
    """主页"""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category_list'
    paginate_by = 5


class AboutView(generic.TemplateView):
    """关于页面"""
    template_name = 'blog/about.html'
