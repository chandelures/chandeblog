import uuid

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def avatar_upload_to(instance, filename):
    filename = '{}.{}'.format(uuid.uuid4().hex, filename.split('.')[-1])
    return 'avatar/{}/{}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to=avatar_upload_to, default='avatar/default.png')

    @staticmethod
    def get_avatar_default():
        return 'avatar/default.png'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        old_avatar = Profile.objects.get(pk=instance.pk).avatar
        new_avatar = instance.avatar
        if old_avatar.name != Profile.get_avatar_default() and new_avatar != old_avatar:
            old_avatar.delete(save=False)


@receiver(pre_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    instance.avatar.delete(save=False)
