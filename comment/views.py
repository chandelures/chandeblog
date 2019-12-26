from django.shortcuts import render
from comment.models import Comment
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from comment.forms import CommentForm
from blog.models import Post


class PostCommentView(View):
    def post(self, request, post_id, parent_comment_id=None):
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return redirect(post.get_absolute_url())

            new_comment.save()
            return redirect(post.get_absolute_url())
        else:
            return HttpResponse("表单内容有误，请重新填写。")
