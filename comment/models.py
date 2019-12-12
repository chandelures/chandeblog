from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from blog.models import Post


class Comment(MPTTModel):
    article = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replyers'
    )
    like = models.PositiveIntegerField('点赞', editable=False, default=0)
    unlike = models.PositiveIntegerField('踩', editable=False, default=0)

    def __str__(self):
        return self.body[:20]

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        app_label = 'comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name
