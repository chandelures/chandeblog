from ..models import Post, Category
from django.db.models.aggregates import Count
from django import template
import markdown

register = template.Library()


@register.simple_tag
def markdown_text(text):
    """markdown渲染"""
    config = {
        'codehilite': {
            'use_pygments': True,
        }
    }
    html = markdown.markdown(text,
                             extensions=[
                                 'markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 "markdown.extensions.toc",
                             ],
                             extensions_configs=config)
    return html
