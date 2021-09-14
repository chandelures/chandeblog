import os
import sys
from pathlib import Path

import django
import faker


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)


fake = faker.Faker('zh_CN')


def clean_database():
    print('clean database')
    Article.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()
    Comment.objects.all().delete()


def create_superuser():
    print('create super user')
    global user
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')


def create_categories():
    print('create categories')
    categories = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    for category in categories:
        Category.objects.create(name=category)


def create_articles():
    print('create some articles by using Faker')

    def section():
        return '## ' + fake.sentence().rstrip('.') + '\n\n' + \
            fake.paragraph(10) + '\n\n' + fake.paragraph(10) + '\n\n'

    def subsection():
        return '### ' + fake.sentence().rstrip('.') + '\n\n' + \
            fake.paragraph(10) + '\n\n' + fake.paragraph(10) + \
            '\n\n' + fake.paragraph(10) + '\n\n'

    def subsections(count):
        results = ''
        for j in range(count):
            results = results + subsection()
        return results

    for i in range(100):
        category = Category.objects.order_by('?').first()
        title = fake.sentence().rstrip('.')
        abstract = fake.paragraph(8) + '\n\n' + fake.paragraph(8) + '\n\n'

        content = "{}".format(abstract + section() + section() +
                              subsections(2) + section() + subsections(3))

        Article.objects.create(
            title=title,
            category=category,
            abstract=abstract,
            content=content,
            author=user,
        )


def create_md_sample_article():
    print('create a sample article')
    Article.objects.create(
        title='博客文章 Markdown 测试',
        abstract=fake.paragraph(),
        content=Path(BASE_DIR).joinpath(
            'scripts', 'example.md').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        author=user,
    )


def create_users():
    print('create some users')
    for i in range(10):
        User.objects.create_user(
            username=fake.name(),
            password='123456',
        )


def create_comments():
    print('create some comments')
    for article in Article.objects.all():
        user = User.objects.all().order_by('?').first()
        for i in range(10):
            Comment.objects.create(
                user=user,
                article=article,
                content=fake.paragraph(),
            )


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chandeblog.settings")
    django.setup()

    from django.contrib.auth import get_user_model
    from comment.models import Comment
    from blog.models import Category, Article
    User = get_user_model()

    clean_database()
    create_superuser()
    create_users()
    create_categories()
    create_articles()
    create_md_sample_article()
    print('done')
