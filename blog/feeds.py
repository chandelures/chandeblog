from django.contrib.syndication.views import Feed

from .models import Article
from chandeblog import settings


class ArticleFeed(Feed):
    """文章RSS"""
    title = settings.RSS_TITLE
    link = '/'
    description = settings.RSS_DISCRIPTION

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract
