from django.urls import path

from comment import views

app_name = 'comment'

urlpatterns = [
    path('<slug:article_slug>',
         views.CommentList.as_view(), name='comment-list'),
    path('<slug:article_slug>/create',
         views.CommentCreate.as_view(), name='comment-create'),
]
