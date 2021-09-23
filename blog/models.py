import uuid
from django.db.models.fields.files import ImageField

from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from uuslug import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, editable=False, max_length=200)
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    abstract = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        to_field="slug",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increase_views(self):
        """使文章浏览数加一"""
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ('-created',)


class About(models.Model):
    article = models.OneToOneField(
        Article, to_field='slug', on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title


def img_upload_to(instance, filename):
    filename = '{}.{}'.format(instance.uid.hex, filename.split('.')[-1])
    return 'img/{}'.format(filename)


class Image(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True,
                           db_index=True, editable=False)
    img = models.ImageField(upload_to=img_upload_to)

    def __str__(self):
        return self.img.name


@receiver(pre_save, sender=Article)
def gen_article_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)


@receiver(pre_save, sender=Category)
def gen_category_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    instance.img.delete(False)


@receiver(pre_save, sender=About)
def about_save(sender, instance, **kwargs):
    instance.pk = 1
