from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Article
from blog.serializers import ArticleDetailSerializer

User = get_user_model()


class ArticleDetailSerializerTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        for i in range(3):
            Article.objects.create(
                title='测试标题{}'.format(i),
                abstract='测试内容',
                content='测试内容',
                author=user,
            )
        self.articles = Article.objects.all().order_by('id')

    def test_next_and_previous(self) -> None:
        serializer = ArticleDetailSerializer(self.articles.first())
        self.assertTrue('next' in serializer.data)
        self.assertTrue('previous' in serializer.data)
        self.assertEqual(self.articles[1].slug, serializer.data['next'])
        self.assertEqual(None, serializer.data['previous'])

        serializer = ArticleDetailSerializer(self.articles.last())
        self.assertTrue('next' in serializer.data)
        self.assertTrue('previous' in serializer.data)
        self.assertEqual(self.articles[1].slug, serializer.data['previous'])
        self.assertEqual(None, serializer.data['next'])
