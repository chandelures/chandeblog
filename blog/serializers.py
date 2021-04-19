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
    category_name = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.username')
    avatar = serializers.ReadOnlyField(source='author.profile.avatar.url')
    title = serializers.CharField(required=False)
    abstract = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Article
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'slug', 'name', 'created')
