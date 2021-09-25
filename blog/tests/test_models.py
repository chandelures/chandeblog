from django.test import TestCase
from django.contrib.auth import get_user_model

from uuslug import slugify

from blog.models import Article, Category, About

User = get_user_model()


class ArticleModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.article = Article.objects.create(
            title='测试标题',
            abstract='测试内容',
            content='测试内容',
            author=user,
        )

    def test_str_representation(self) -> None:
        self.assertEqual(self.article.__str__(), self.article.title)

    def test_generate_slug(self) -> None:
        self.assertEqual(self.article.slug, slugify(self.article.title))

    def test_increase_views(self) -> None:
        self.article.increase_views()
        self.article.refresh_from_db()
        self.assertEqual(self.article.views, 1)


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="测试分类",
        )

    def test_str_representation(self) -> None:
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_generate_slug(self) -> None:
        self.assertEqual(self.category.slug, slugify(self.category.name))


class AboutModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        article = Article.objects.create(
            title='测试标题',
            abstract='测试内容',
            content='测试内容',
            author=user,
        )
        self.about = About.objects.create(
            article=article,
        )

    def test_str_representation(self) -> None:
        self.assertEqual(self.about.__str__(), self.about.article.title)

    def test_save(self) -> None:
        other_about = About(
            article=self.about.article,
        )
        other_about.save()
        self.assertEqual(self.about, other_about)
