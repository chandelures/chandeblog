# Generated by Django 3.2 on 2021-04-19 14:08

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar/default.png', upload_to=userprofile.models.avatar_upload_to),
        ),
    ]
