from django.urls import re_path

from comment import views

app_name = 'comment'

urlpatterns = [
    re_path(r'^(?P<article_slug>[-\w]+)$',
            views.CommentList.as_view(), name='comment-list'),
    re_path(r'^(?P<article_slug>[-\w]+)/create$',
            views.CommentCreate.as_view(), name='comment-create'),
]
