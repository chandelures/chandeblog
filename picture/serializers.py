from rest_framework import serializers

from picture.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        exclude = ('id', )