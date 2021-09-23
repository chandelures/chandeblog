from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    uid = serializers.ReadOnlyField(source='profile.uid')
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    isAdmin = serializers.ReadOnlyField(source='is_staff')

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    def update(self, instance, validated_data) -> User:
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('uid', 'username', 'password', 'email',
                  'avatar', 'last_login', 'isAdmin')
        read_only_fields = ('last_login', )
