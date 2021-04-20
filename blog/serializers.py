from rest_framework import serializers
from blog.models import Article, Category, Image


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
    avatar = serializers.ImageField(
        source='author.profile.avatar', read_only=True)
    title = serializers.CharField(required=False)
    abstract = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    previous = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    def get_previous(self, obj):
        previous_obj = Article.objects.filter(
            pk__lt=obj.pk).all().order_by('-id').first()
        if previous_obj:
            return previous_obj.slug
        else:
            return None

    def get_next(self, obj):
        next_obj = Article.objects.filter(
            pk__gt=obj.pk).all().order_by('id').first()
        if next_obj:
            return next_obj.slug
        else:
            return None

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


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
