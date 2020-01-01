from comment.models import Comment
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from comment.forms import CommentForm
from blog.models import Post
from notifications.signals import notify

User = get_user_model()


class PostCommentView(View):
    @method_decorator(login_required)
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
                # if not parent_comment.user.is_superuser:
                #     notify.send(
                #         request.user,
                #         recipient=parent_comment.user,
                #         verb='回复了你',
                #         target=post,
                #         action_object=new_comment,
                #     )
                return redirect(post.get_absolute_url() +
                                '#comment_' + str(new_comment.parent_id))

            new_comment.save()

            # if not request.user.is_superuser:
            #     notify.send(
            #         request.user,
            #         recipient=User.objects.filter(is_superuser=1),
            #         verb='回复了你',
            #         target=post,
            #         action_object=new_comment,
            #     )

            return redirect(post.get_absolute_url() +
                            '#comment_' + str(new_comment.id))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
