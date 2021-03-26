from rest_framework import serializers
from blog.models import Article, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, view_name='blog:article-detail', read_only=True, lookup_field='slug')

    class Meta:
        model = Category
        fields = ('slug', 'name', 'articles', 'created')


class ArticleListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('slug', 'id', 'title', 'created', 'author',
                  'category', 'abstract', 'views')


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('slug', 'id', 'title', 'created', 'author', 'category', 'views', 'content')
