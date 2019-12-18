from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import UserManager

from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    """用户个人信息

    Attributes:
        nickname: 昵称
        link: 个人网站的网址
        avatar: 头像
        resume： 简介

    """
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称')
    link = models.URLField('个人网址', blank=True)
    resume = models.TextField(max_length=500, blank=True)
    avatar = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                 processors=[ResizeToFill(100, 100)],
                                 format='JPEG',
                                 options={'quality': 95}
                                 )

    def save(self, *args, **kwargs):
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        super(User, self).save()

    def __str__(self):
        return self.username

    class Meta:
        app_label = "userprofile"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
