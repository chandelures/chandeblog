from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Article
from comment.models import Comment

User = get_user_model()


class CommentModelTest(TestCase):
    def setUp(self) -> None:
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
            user=self.user,
        )
        self.child_comment = Comment.objects.create(
            content='测试评论',
            article=self.article,
            user=self.test_user,
            parent=self.comment
        )

    def test_str_representation(self) -> None:
        self.assertEqual(self.comment.__str__(), self.comment.content[:20])

    def test_is_root(self) -> None:
        self.assertTrue(self.comment.is_root)

    def test_is_leaf(self) -> None:
        self.assertTrue(self.child_comment.is_leaf)

    def test_create_childen_comment(self) -> None:
        other_child_comment = Comment.objects.create(
            content='测试评论',
            article=self.article,
            user=self.user,
            parent=self.child_comment,
        )
        self.assertEqual(other_child_comment.parent, self.comment)
        self.assertEqual(other_child_comment.reply, self.child_comment.user)
