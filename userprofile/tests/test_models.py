from io import BytesIO
from PIL import Image as Ima
from pathlib import Path

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.base import File

User = get_user_model()


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )

    @staticmethod
    def get_avatar_file(name='avatar.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Ima.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @staticmethod
    def gen_default_avatar(size=(50, 50), color=(256, 0, 0)):
        image = Ima.new('RGBA', size=size, color=color)
        with open('media/avatar/default.png', 'wb') as f:
            image.save(f, 'png')

    def test_str_representation(self):
        self.assertEqual(self.user.profile.__str__(), self.user.username)

    def test_profile_create(self):
        self.assertIsNotNone(self.user.profile)

    def test_upload_avatar(self):
        self.user.profile.avatar = self.get_avatar_file()
        self.user.profile.save()
        self.user.profile.refresh_from_db()
        self.assertTrue(Path(self.user.profile.avatar.path).exists())

    def test_change_avatar(self):
        self.gen_default_avatar()

        default_path = self.user.profile.avatar.path
        self.user.profile.avatar = self.get_avatar_file()
        self.user.profile.save()
        self.assertTrue(Path(default_path).exists())

        old_path = self.user.profile.avatar.path
        self.user.profile.avatar = self.get_avatar_file()
        self.user.profile.save()
        self.assertFalse(Path(old_path).exists())

    def test_delete_avatar(self):
        avatar_path = self.user.profile.avatar.path
        self.user.delete()
        self.user.save()
        self.assertFalse(Path(avatar_path).exists())

    def tearDown(self):
        self.user.delete()
        self.user.save()
