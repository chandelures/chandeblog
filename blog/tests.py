from django.test import TestCase
from .models import *


class PostTestCase(TestCase):
    def setUp(self) -> None:
        c1 = Category.objects.create(name="test1")
        t1 = Tag.objects.create(name="test1")
        p1 = Post.objects.create(title="test1", body="# Test1", summary="# Test1", category=c1)

    def test_echo(self):
        self.assertEqual(True, True)

