# Generated by Django 3.1.7 on 2021-03-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar/default/default.png', upload_to='avatar/'),
        ),
    ]
