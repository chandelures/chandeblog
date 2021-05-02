from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models import Article

from comment.models import Comment

User = get_user_model()


class ChildCommentSerializer(serializers.ModelSerializer):
    userName = serializers.ReadOnlyField(source='user.username')
    replyName = serializers.ReadOnlyField(source='reply.username')

    class Meta:
        model = Comment
        exclude = ('article', 'parent', 'user', 'reply')


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), write_only=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    userName = serializers.ReadOnlyField(source='user.username')
    children = ChildCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        exclude = ('reply', )
