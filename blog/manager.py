from django.db import models


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
