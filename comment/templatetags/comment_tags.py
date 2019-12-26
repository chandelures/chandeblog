from comment.models import Comment
from comment.forms import CommentForm
from django.db.models.aggregates import Count
from django import template

register = template.Library()


@register.simple_tag
def get_comments(post_id):
    comments = Comment.objects.filter(post=post_id)
    return comments


@register.simple_tag
def get_comments_count(post_id):
    count = Comment.objects.filter(post=post_id).count()
    return count
