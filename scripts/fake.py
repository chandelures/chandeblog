import os
import sys
from datetime import timedelta
from pathlib import Path

import django
import faker
from django.utils import timezone


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chandeblog.settings")
    django.setup()

    from django.contrib.auth import get_user_model
    from blog.models import Category, Article

    User = get_user_model()

    print('clean database')
    Article.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()

    print('create super user')
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    categories = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    a_year_ago = timezone.now() - timedelta(days=365)

    print('create categories')
    for category in categories:
        Category.objects.create(name=category)

    print('create some articles by using Faker')
    fake = faker.Faker('zh_CN')
    for i in range(100):
        category = Category.objects.order_by('?').first()
        created = fake.date_time_between(
            start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
        Article.objects.create(
            title=fake.sentence().rstrip('.'),
            category=Category.objects.order_by('?').first(),
            abstract='\n\n'.join(fake.paragraphs(3)),
            content='\n\n'.join(fake.paragraphs(10)),
            created=created,
        )

    print('create a sample article')
    Article.objects.create(
        title='博客文章 Markdown 测试',
        abstract='博客文章 Markdown 测试',
        content=Path(BASE_DIR).joinpath(
            'scripts', 'example.md').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试')
    )

    print('done')
