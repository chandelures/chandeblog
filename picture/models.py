import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def img_upload_to(instance, filename) -> str:
    filename = '{}.{}'.format(instance.uid.hex, filename.split('.')[-1])
    return 'img/{}'.format(filename)


class Image(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True,
                           db_index=True, editable=False)
    img = models.ImageField(upload_to=img_upload_to)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.img.name

    class Meta:
        ordering = ('-created',)


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs) -> None:
    instance.img.delete(False)
