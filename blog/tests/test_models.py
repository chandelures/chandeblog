from io import BytesIO
from PIL import Image as Ima
from pathlib import Path

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.base import File

from uuslug import slugify

from blog.models import Article, Category, About, Image

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


class ImageModelTest(TestCase):
    def setUp(self) -> None:
        self.image = Image.objects.create(
            img=self.get_image_file()
        )

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50),
                       color=(256, 0, 0)) -> File:
        file_obj = BytesIO()
        image = Ima.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_str_representation(self) -> None:
        self.assertEqual(self.image.__str__(), self.image.img.name)

    def test_delete(self) -> None:
        img_path = self.image.img.path
        self.image.delete()
        self.assertFalse(Path(img_path).exists())

    def tearDown(self) -> None:
        if self.image.pk:
            self.image.delete()
