from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False, max_length=200)
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    abstract = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    views = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def increase_views(self):
        """使文章浏览数加一"""
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ('-created',)


class About(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)

    def __str__(self):
        return "About"

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)
