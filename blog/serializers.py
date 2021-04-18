from rest_framework import serializers
from blog.models import Article, Category


class ArticleListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('slug', 'id', 'title', 'created', 'updated', 'author',
                  'category', 'abstract', 'views')


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.username')
    avatar = serializers.ReadOnlyField(source='author.profile.avatar.url')

    class Meta:
        model = Article
        fields = ('slug', 'id', 'title', 'created', 'updated',
                  'author', 'avatar', 'category', 'views', 'content')


class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name', 'created')
