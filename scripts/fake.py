from django.core.exceptions import ImproperlyConfigured
import os
import sys
from pathlib import Path

import django
import faker


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)


fake = faker.Faker('zh_CN')

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chandeblog.settings")
    django.setup()

    from django.contrib.auth import get_user_model
    from comment.models import Comment
    from blog.models import Category, Article, About
    User = get_user_model()
except ImproperlyConfigured:
    pass


def clean_database() -> None:
    print('clean database')
    Article.objects.all().delete()
    About.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()
    Comment.objects.all().delete()


def create_superuser() -> None:
    print('create super user')
    global user
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')


def create_categories() -> None:
    print('create categories')
    categories = ['test1', 'test2', 'test3', 'test4', 'test5']
    for category in categories:
        Category.objects.create(name=category)


def create_articles() -> None:
    print('create some articles by using Faker')

    def section() -> str:
        return '## {}\n\n{}\n\n{}\n\n'.format(
            fake.sentence().rstrip('.'),
            fake.paragraph(10), fake.paragraph(10)
        )

    def subsection() -> str:
        return '### {}\n\n{}\n\n{}\n\n{}\n\n'.format(
            fake.sentence().rstrip('.'),
            fake.paragraph(10),
            fake.paragraph(10),
            fake.paragraph(10)
        )

    def subsections(count) -> str:
        results = ''
        for _ in range(count):
            results = results + subsection()
        return results

    for _ in range(100):
        category = Category.objects.order_by('?').first()
        title = fake.sentence().rstrip('.')
        abstract = '{}\n\n{}\n\n'.format(fake.paragraph(8), fake.paragraph(8))
        content = "{}".format(abstract + section() + section() +
                              subsections(2) + section() + subsections(3))

        Article.objects.create(
            title=title,
            category=category,
            abstract=abstract,
            content=content,
            author=user,
        )


def create_md_sample_article() -> None:
    print('create a sample article')
    Article.objects.create(
        title='博客文章 Markdown 测试',
        abstract=Path(BASE_DIR).joinpath(
            'scripts', 'abstract.md').read_text(encoding='utf-8'),
        content=Path(BASE_DIR).joinpath(
            'scripts', 'example.md').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        author=user,
    )


def create_about() -> None:
    print('create about article')
    About.objects.create(
        article=Article.objects.all().order_by('?').first()
    )


def create_users() -> None:
    print('create some users')
    for _ in range(10):
        User.objects.create_user(
            username=fake.name(),
            password='123456',
        )


def create_comments() -> None:
    print('create some comments')
    article = Article.objects.first()
    user = User.objects.all().order_by('?').first()
    for _ in range(10):
        root = Comment.objects.create(
            user=user,
            article=article,
            content=fake.paragraph(),
        )
        leaf = Comment.objects.create(
            user=User.objects.all().order_by('?').first(),
            article=article,
            content=fake.paragraph(),
            parent=root,
        )
        Comment.objects.create(
            user=User.objects.all().order_by('?').first(),
            article=article,
            content=fake.paragraph(),
            parent=leaf,
        )


def main() -> None:
    clean_database()
    create_superuser()
    create_users()
    create_categories()
    create_articles()
    create_about()
    create_md_sample_article()
    create_comments()
    print('done')


if __name__ == '__main__':
    main()
