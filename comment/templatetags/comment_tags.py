from comment.models import Comment
from comment.forms import CommentForm
from django import template
import time

register = template.Library()


@register.simple_tag
def get_comment_children_count(comment):
    count = comment.get_children().count()
    return count


@register.simple_tag
def get_comment_form():
    comment_form = CommentForm()
    return comment_form


@register.filter
def time_since(value):
    now = time.time()
    diff_timestamp = now - value.timestamp()
    if diff_timestamp < 60:
        return "刚刚"
    elif diff_timestamp >= 60 and diff_timestamp < 60 * 60:
        minutes = int(diff_timestamp / 60)
        return "%s分钟前" % minutes
    elif diff_timestamp >= 60 * 60 and diff_timestamp < 60 * 60 * 24:
        hours = int(diff_timestamp / (60 * 60))
        return "%s小时前" % hours
    elif diff_timestamp >= 60 * 60 * 24 and diff_timestamp < 60 * 60 * 24 * 30:
        days = int(diff_timestamp / (60 * 60 * 24))
        return "%s天前" % days
    else:
        return value.strftime("%Y/%m/%d")
