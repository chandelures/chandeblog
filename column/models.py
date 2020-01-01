from django.db import models
from uuslug import slugify


class Column(models.Model):
    """专栏模型

    Attributes:
        name: 名称.
        slug: url字符串.
        create_date: 创建日期
        cover: 封面图片

    """
    name = models.CharField(verbose_name='名称', max_length=20)
    slug = models.SlugField(editable=False)
    create_date = models.DateTimeField('创建日期', auto_now_add=True, null=True)
    cover = models.ImageField(
        verbose_name="封面图片",
        null=False,
        upload_to="column/cover")
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        null=True,
        on_delete=models.SET_NULL,
        related_name='post'
    )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('blog:column', args=[self.slug])

    def save(self, *args, **kwargs):
        """自动保存slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """栏目分类模型

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

    # def get_absolute_url(self):
    #     return reverse('blog:category', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
