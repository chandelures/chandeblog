from rest_framework import serializers
from blog.models import Article, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, view_name='blog:article-detail', read_only=True, lookup_field='slug')

    class Meta:
        model = Category
        fields = ('url', 'slug', 'name', 'articles', 'created')
        extra_kwargs = {
            'url': {'view_name': 'blog:category-detail', 'lookup_field': 'slug'}
        }


class ArticleListSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = ('url', 'slug', 'id', 'title', 'created',
                  'category', 'abstract', 'views')
        extra_kwargs = {
            'url': {'view_name': 'blog:article-detail', 'lookup_field': 'slug'}
        }


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = '__all__'
