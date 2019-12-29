from ..models import Post, Category
from django.db.models.aggregates import Count
from django.utils.html import strip_tags
from django import template

import markdown

register = template.Library()


@register.simple_tag
def markdown_text(text):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
    ])
    html = md.convert(text)
    return html


@register.simple_tag
def get_post_tags(post):
    result = ''
    tags = post.tags.all()
    for tag in tags:
        result += tag.name
        if tag != tags.last():
            result += ","
    return result


@register.simple_tag
def get_descriptions(text):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
    ])
    return strip_tags(md.convert(text)).replace("\n", "")
