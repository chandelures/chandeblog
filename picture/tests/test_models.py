from PIL import Image as Ima
from io import BytesIO
from pathlib import Path

from django.core.files.base import File
from django.test import TestCase

from picture.models import Image


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
