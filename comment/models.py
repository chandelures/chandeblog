from django.db import models
from blog.models import Post
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(MPTTModel):
    """评论模型

    Attributes:
        article: 评论所属文章
        user: 发表评论用户
        body: 评论内容
        create_date: 创建日期
        parent: 父评论对象
        reply_to: 回复的用户
        like: 点赞的数量
        unlike: 点踩的数量
    """
    post = models.ForeignKey(
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
    create_date = models.DateTimeField(auto_now_add=True)
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
        return self.user.username + ": " + self.body[:10]

    class MPTTMeta:
        order_insertion_by = ['create_date']

    class Meta:
        app_label = 'comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name
