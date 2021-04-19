from django.shortcuts import get_object_or_404

from rest_framework import generics

from blog.models import Article, Category, About
from blog.serializers import ArticleListSerializer
from blog.serializers import ArticleDetailSerializer
from blog.serializers import CategoryDetailSerializer, CategoryListSerializer

from blog.paginations import PageNumberPagination
from blog.permissions import IsAdminUserOrReadOnly


class CategoryList(generics.ListAPIView):
    """
    列出所有分类
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    分类的查询
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class CategoryCreate(generics.CreateAPIView):
    """
    分类的创建

    * 只有管理员可以进行操作
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class ArticleList(generics.ListAPIView):
    """
    列出所有文章
    """
    queryset = Article.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = ArticleListSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    文章的查询
    """
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        article.increase_views()
        return super().get(request, *args, **kwargs)


class ArticleCreate(generics.CreateAPIView):
    """
    文章的创建

    * 只有管理员可以进行操作
    """
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class AboutDetail(generics.RetrieveAPIView):
    """
    获取About的相关信息
    """
    queryset = About.objects.all()
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        about = get_object_or_404(self.queryset, pk=1)
        return about.article
