from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from blog.models import Article, Category
from blog.serializers import ArticleListSerializer
from blog.serializers import ArticleDetailSerializer
from blog.serializers import CategorySerializer

from blog.paginations import PageNumberPagination
from blog.permissions import IsAdminUserOrReadOnly


class ApiRoot(APIView):
    """
    列出所有api路径

    * 只有管理员可以访问
    """
    permission_classes = (IsAdminUser, )

    def get(self, request):
        """
        返回api路径
        """
        return Response({
            'articles': reverse('blog:article-list', request=request),
            'category': reverse('blog:category-list', request=request),
            'create': {
                'article': reverse('blog:article-create', request=request),
                'category': reverse('blog:category-create', request=request),
            },
        })


class CategoryList(generics.ListAPIView):
    """
    列出所有分类
    """
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    分类的查询、更新和删除

    * 只有管理员可以进行更新与删除操作
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class CategoryCreate(generics.CreateAPIView):
    """
    分类的创建

    * 只有管理员可以进行操作
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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
    文章的查询、更新和删除

    * 只有管理员可以进行更新和删除操作
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
