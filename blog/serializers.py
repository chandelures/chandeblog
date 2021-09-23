from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

from blog.models import Article, Category

User = get_user_model()


class ArticleListSerializer(serializers.ModelSerializer):
    categoryName = serializers.ReadOnlyField(source='category.name')
    authorName = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        exclude = ('id', 'content', 'category', 'author')


class ArticleDetailSerializer(serializers.ModelSerializer):
    categoryName = serializers.ReadOnlyField(source='category.name')
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )
    authorName = serializers.ReadOnlyField(source='author.username')
    avatar = serializers.ImageField(
        source='author.profile.avatar', read_only=True)
    previous = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_previous(self, obj) -> str:
        previous_obj = Article.objects.filter(
            pk__lt=obj.pk).all().order_by('-id').first()
        if previous_obj:
            return previous_obj.slug
        else:
            return None

    def get_next(self, obj) -> str:
        next_obj = Article.objects.filter(
            pk__gt=obj.pk).all().order_by('id').first()
        if next_obj:
            return next_obj.slug
        else:
            return None

    def get_comments(self, obj) -> str:
        return reverse('comment:comment-list',
                       kwargs={'article_slug': obj.slug})

    class Meta:
        model = Article
        exclude = ('id',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        exclude = ('id',)


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
