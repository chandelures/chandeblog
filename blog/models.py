from django.db import models
from django.shortcuts import reverse

from uuslug import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    slug = models.SlugField(editable=False, unique=True)
    title = models.CharField(max_length=100, unique=True)
    abstract = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        blank=True,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    views = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('api:article-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def increase_views(self):
        """使文章浏览数加一"""
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ('-created',)
