import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chandeblog.settings")
    django.setup()

    from blog.models import Category, Post
    from column.models import Column
    from comment.models import Comment
    from django.contrib.auth import get_user_model

    User = get_user_model()
    from taggit.models import Tag

    print('clean database')
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()
    Column.objects.all().delete()

    print('create a blog user')
    user = User.objects.create_superuser('admin', 'admin@hellogithub.com', 'admin')

    category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx', 'Elasticsearch', 'Gunicorn', 'Supervisor', 'test tag']
    a_year_ago = timezone.now() - timedelta(days=365)

    column_list = ['python学习笔记', 'c++学习笔记', 'c语言学习笔记', 'c#学习笔记']

    fake = faker.Faker('zh-cn')

    print('create columns, categories and tags')
    for col in column_list:
        Column.objects.create(name=col)

    for cate in category_list:
        Category.objects.create(name=cate)

    for tag in tag_list:
        Tag.objects.create(name=tag)

    print('create some faked posts published within the past year')
    for i in range(40):
        column = Column.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        cate = Category.objects.order_by('?').first()
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            abstract='\n'.join(fake.paragraphs(3)),
            create_date=created_time,
            column=column,
            column_position=i,
            category=cate,
            author=user,
            status=True,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create a markdown sample post')
    Post.objects.create(
        title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'post_body.md').read_text(encoding='utf-8'),
        abstract=pathlib.Path(BASE_DIR).joinpath('scripts', 'post_abstract.md').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        author=user,
        status=True,
    )

    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created_time = post.create_date
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                body=fake.paragraph(),
                user=user,
                create_date=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )

    print('done!')
