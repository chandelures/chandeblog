from django.contrib.syndication.views import Feed
from django.shortcuts import reverse

from chandeblog import settings
from .models import Article


class ArticleFeed(Feed):
    """文章RSS"""
    title = settings.RSS_TITLE
    description = settings.RSS_DISCRIPTION
    link = settings.RSS_LINK_HOST

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    def item_link(self, item):
        return self.link + reverse('blog:article-detail', args=(item.slug, ))
