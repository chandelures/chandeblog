from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source='profile.avatar.url')
    password = serializers.CharField(write_only=True)
    isAdmin = serializers.ReadOnlyField(source='is_staff')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'avatar', 'last_login', 'isAdmin')
        read_only_fields = ('last_login', )
