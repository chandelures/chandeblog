import uuid

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def avatar_upload_to(instance, filename) -> str:
    filename = '{}.{}'.format(uuid.uuid4().hex, filename.split('.')[-1])
    return 'avatar/{}/{}'.format(instance.user.username, filename)


def avatar_default() -> str:
    return 'avatar/default.png'


class Profile(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True,
                           db_index=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to=avatar_upload_to, default=avatar_default)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs) -> None:
    if instance.pk:
        old_avatar = Profile.objects.get(pk=instance.pk).avatar
        new_avatar = instance.avatar
        if (old_avatar.name != avatar_default()
                and new_avatar != old_avatar):
            old_avatar.delete(save=False)


@receiver(pre_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    if instance.avatar != avatar_default():
        instance.avatar.delete(save=False)
