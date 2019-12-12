from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    resume = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

    class Meta:
        app_label = 'userprofile'
        verbose_name = "用户配置"
        verbose_name_plural = verbose_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    instance.profile.delete()