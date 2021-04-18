from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source='profile.avatar.url')
    is_admin = serializers.ReadOnlyField(source='is_superuser')

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'avatar', 'last_login', 'is_admin', 'is_superuser')
