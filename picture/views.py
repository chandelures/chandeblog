from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from picture.models import Image
from picture.serializers import ImageSerializer


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)


class ImageUpload(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'uid'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)
