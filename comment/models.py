from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save

from blog.models import Article

User = get_user_model()


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
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
def comment_post_save_receiver(sender, instance, **kwargs):
    if instance.parent and instance.parent.parent:
        instance.parent = instance.parent.parent
