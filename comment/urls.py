from django.urls import path
from comment import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:post_id>/', views.PostCommentView.as_view(), name='post_comment'),
    path('post-comment/<int:post_id>/<int:parent_comment_id>', views.PostCommentView.as_view(), name='comment_reply')
]
