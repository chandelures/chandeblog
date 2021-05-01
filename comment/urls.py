from django.urls import path, re_path

from comment import views

app_name = 'comment'

urlpatterns = [
    re_path(r'^(?P<article_id>[0-9]+)$',
            views.CommentList.as_view(), name='comment-list'),
    re_path(r'^(?P<article_id>[0-9]+)/create$',
            views.CommentCreate.as_view(), name='comment-create'),
]
