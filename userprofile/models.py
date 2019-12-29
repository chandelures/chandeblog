from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户个人信息
    Attributes:
        link: 个人网站的网址
        resume： 简介
    """
    link = models.URLField('个人网址', blank=True)
    resume = models.TextField('简介', max_length=500, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = "userprofile"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
