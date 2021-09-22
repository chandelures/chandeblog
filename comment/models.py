import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import BooleanField
from django.dispatch import receiver
from django.db.models.signals import pre_save

from blog.models import Article

User = get_user_model()


class Comment(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4,
                           db_index=True, editable=False)
    article = models.ForeignKey(
        Article,
        to_field='slug',
        on_delete=models.CASCADE,
        related_name='comment',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        to_field='uid',
        on_delete=models.CASCADE,
        null=True,
        related_name='children',
    )
    reply = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='replied',
    )
    tag = BooleanField(choices=[(0, 'root'), (1, 'leaf')], default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.content[:20]

    @property
    def is_root(self):
        if self.parent:
            return False
        else:
            return True


@receiver(pre_save, sender=Comment)
def pre_save_comment(sender, instance, **kwargs):
    if instance.parent:
        instance.reply = instance.parent.user
        if instance.parent.parent:
            instance.parent = instance.parent.parent
