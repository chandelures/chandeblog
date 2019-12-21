from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from blog.models import Post


class BlogFeed(Feed):
    title = 'Chandelure的个人博客'
    description = 'Chandelure的个人博客'
    link = "/rss/"

    def items(self):
        return Post.objects.public()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract[:50] + "......"

    def item_link(self, item):
        return reverse('blog:post', args=(item.id,))
