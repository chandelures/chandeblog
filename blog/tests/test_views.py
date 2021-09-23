from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Article, About

User = get_user_model()


class ApiRootViewTest(TestCase):
    def setUp(self) -> None:
        self.apiclient = APIClient()
        self.url = reverse('blog:api-root')

    def test_api_root(self) -> None:
        response = self.apiclient.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArticleDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.apiclient = APIClient()
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
        self.url = reverse('blog:article-detail',
                           kwargs={'slug': self.article.slug})

    def test_increase_views(self) -> None:
        response = self.apiclient.get(self.url)
        self.article.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.views, 1)


class ArticleCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.apiclient = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.url = reverse('blog:article-create')

    def test_create(self) -> None:
        data = {
            'title': '测试文章',
            'abstract': '测试内容',
            'content': '测试内容',
        }

        response = self.apiclient.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apiclient.login(username='admin', password='admin')
        response = self.apiclient.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AboutViewTest(TestCase):
    def setUp(self) -> None:
        self.apiclient = APIClient()
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
        About.objects.create(article=article)
        self.url = reverse('blog:about')

    def test_about(self) -> None:
        response = self.apiclient.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
