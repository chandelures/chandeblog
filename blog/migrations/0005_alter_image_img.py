# Generated by Django 3.2 on 2021-04-19 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='img/'),
        ),
    ]