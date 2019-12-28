from ..models import Post, Category
from django.db.models.aggregates import Count
from django import template
import markdown
from markdown.extensions.toc import TocExtension

register = template.Library()


@register.simple_tag
def markdown_text(text):
    config = {
        'codehilite': {
            'use_pygments': False,
        },
    }
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ],
        extensions_configs=config)
    html = md.convert(text)
    return html


@register.simple_tag
def get_post_tags(post):
    result = ''
    tags = post.tags.all()
    for tag in tags:
        result += tag.name
        if tag != tags.last():
            result += ", "
    return result
