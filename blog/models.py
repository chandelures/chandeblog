from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import django.utils.timezone as timezone
from uuslug import slugify


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class DraftPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=False)


class Post(models.Model):
    """文章"""
    title = models.CharField(verbose_name='标题', max_length=100)
    slug = models.SlugField(editable=False)
    author = models.ForeignKey(
        User,
        verbose_name='作者',
        null=True,
        on_delete=models.SET_NULL,
        auto_created=True)
    cover = models.ImageField(
        verbose_name='封面图片',
        null=True,
        upload_to='cover')
    summary = models.TextField(verbose_name='摘要')
    body = models.TextField(verbose_name='正文')
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        null=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    views = models.PositiveIntegerField('浏览量', default=0)
    create_date = models.DateTimeField('创建日期', default=timezone.now)
    mod_time = models.DateTimeField('最后修改时间', auto_now=True)
    STATUS_CHOICE = ((False, '草稿'), (True, '发布'))
    status = models.BooleanField('状态', default=False, choices=STATUS_CHOICE)

    objects = models.Manager()
    public_objects = PostManager()
    draft = DraftPostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'blog'
        ordering = ['-create_date']
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """分类"""
    name = models.CharField(verbose_name='名称', max_length=20)
    slug = models.SlugField(editable=False)
    create_date = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now)
    mod_date = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    # objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签"""
    name = models.CharField(verbose_name='名称', max_length=20)
    slug = models.SlugField(editable=False)
    create_date = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now)
    mod_date = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    # objects = TagManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
