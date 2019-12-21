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
            'use_pygments': True,
        },
        'toc': {
            'toc_depth': 3,
        }
    }
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        "markdown.extensions.toc",
    ],
        extensions_configs=config)
    html = md.convert(text)
    return {
        "html": html,
        "toc": md.toc
    }
