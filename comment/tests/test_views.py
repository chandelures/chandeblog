from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from blog.models import Article
from comment.models import Comment


User = get_user_model()


class CommentListViewTest(TestCase):
    def setUp(self):
        self.apicilent = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.test_user = User.objects.create_user(
            username='test',
            password='test',
        )
        self.article = Article.objects.create(
            title='测试标题',
            abstract='测试内容',
            content='测试内容',
            author=self.user,
        )
        self.comment = Comment.objects.create(
            content='测试评论',
            article=self.article,
            user=self.user
        )
        self.child_comment = Comment.objects.create(
            content='测试评论',
            article=self.article,
            user=self.test_user,
            parent=self.comment
        )
        self.url = reverse('comment:comment-list',
                           kwargs={'article_slug': self.article.slug})

    def test_get_comment_list(self):
        response = self.apicilent.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for comment in response.data['results']:
            obj = Comment.objects.get(uid=comment['uid'])
            self.assertTrue(obj.is_root)
            self.assertEqual(obj.article, self.article)
            for child_comment in comment['children']:
                _obj = Comment.objects.get(uid=child_comment['uid'])
                self.assertTrue(_obj.is_leaf)
                self.assertEqual(_obj.article, self.article)


class CommentCreateViewTest(TestCase):
    def setUp(self):
        self.apicilent = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.article = Article.objects.create(
            title='测试标题',
            abstract='测试内容',
            content='测试内容',
            author=self.user,
        )
        self.url = reverse('comment:comment-create',
                           kwargs={'article_slug': self.article.slug})

    def test_comment_create(self):
        data = {
            'content': '测试评论',
        }

        response = self.apicilent.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.apicilent.login(username='admin', password='admin')
        response = self.apicilent.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'content': '测试评论',
            'parent': response.data['uid'],
        }
        response = self.apicilent.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
