from taggit.managers import TaggableManager
from django.db import models

from django.urls import reverse
import django.utils.timezone as timezone

from mdeditor.fields import MDTextField
from uuslug import slugify

from userprofile.models import User


class PostQuerySet(models.QuerySet):
    """文章查询类"""

    def public(self):
        """返回所有状态为公开的文章"""
        return self.filter(status=True)

    def draft(self):
        """返回所有状态为草稿的文章"""
        return self.filter(status=False)


class PostManager(models.Manager):
    """文章管理类"""

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def public(self):
        """返回所有状态为公开的文章"""
        return self.get_queryset().public()

    def draft(self):
        """返回所有状态为草稿的文章"""
        return self.get_queryset().draft()


class Post(models.Model):
    """文章模型

    Attributes:
        title: 文章标题
        slug: url字符串
        author: 作者
        abstrace: 摘要
        body: 正文
        category: 分类
        tags: 标签
        column: 专栏
        views: 浏览量
        create_date: 创建日期
        mod_date: 最后修改日期
        status: 文章的状态（True = 发布， False = 草稿）

    """
    title = models.CharField(verbose_name='标题', max_length=100)
    slug = models.SlugField(editable=False)
    author = models.ForeignKey(
        User,
        verbose_name='作者',
        null=True,
        on_delete=models.SET_NULL,
        auto_created=True)
    abstract = models.TextField(verbose_name='摘要')
    body = MDTextField(verbose_name='正文')
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        null=True,
        on_delete=models.SET_NULL,
        related_name='post'
    )
    tags = TaggableManager()
    # column = models.ForeignKey(
    #     'Column',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     verbose_name="栏目",
    #     related_name='post'
    # )

    views = models.PositiveIntegerField('浏览量', default=0)
    create_date = models.DateTimeField('创建日期', default=timezone.now)
    mod_time = models.DateTimeField('最后修改时间', auto_now=True)
    STATUS_CHOICE = ((False, '草稿'), (True, '发布'))
    status = models.BooleanField('状态', default=False, choices=STATUS_CHOICE)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.slug])

    def save(self, *args, **kwargs):
        """自动保存slug"""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'blog'
        ordering = ['-create_date']
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """分类模型

    Attributes:
        name: 名称.
        slug: url字符串.
        create_date: 创建日期

    """
    name = models.CharField(verbose_name='名称', max_length=20)
    slug = models.SlugField(editable=False)
    create_date = models.DateTimeField('创建日期', auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """自动保存slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
