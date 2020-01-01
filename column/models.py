from django.db import models
from uuslug import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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
    cover = ProcessedImageField(
        upload_to='column', default='column/default.png', verbose_name='封面',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 95})
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        null=True,
        on_delete=models.SET_NULL,
        related_name='post'
    )

    def __str__(self):
        return self.name

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
