from django.utils.html import strip_tags
from django import template

from chandeblog import settings

import markdown

register = template.Library()


@register.simple_tag
def markdown_text(text):
    config = {
        'toc': {
            'toc_depth': 3,
        }
    }
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.toc'
    ], extension_configs=config)
    html = md.convert(text)
    return {
        "html": html,
        "toc": md.toc
    }


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


@register.simple_tag
def get_setting_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def sort_posts_in_column(posts):
    return posts.order_by("column_position")
