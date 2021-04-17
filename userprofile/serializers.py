from rest_framework import serializers

from userprofile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    avatar = serializers.ReadOnlyField(source='avatar.url')
    last_login = serializers.ReadOnlyField(source='user.last_login')
    is_admin = serializers.ReadOnlyField(source='user.is_superuser')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'email',
                  'avatar', 'last_login', 'is_admin')
