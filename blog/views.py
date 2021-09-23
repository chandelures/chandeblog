from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from blog.models import Article, Category, About, Image
from blog.serializers import ArticleListSerializer
from blog.serializers import ArticleDetailSerializer
from blog.serializers import CategoryDetailSerializer, CategoryListSerializer
from blog.serializers import ImageSerializer

from userprofile.permissions import IsAdminUserOrReadOnly


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'article-list': reverse('blog:article-list', request=request,
                                    format=format),
            'category-list': reverse('blog:category-list', request=request,
                                     format=format),
            'about': reverse('blog:about', request=request, format=format),
        })


class CategoryList(generics.ListAPIView):
    """
    列出所有分类
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    分类的查询
    '''
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class CategoryCreate(generics.CreateAPIView):
    '''
    分类的创建

    * 只有管理员可以进行操作
    '''
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class ArticleList(generics.ListAPIView):
    '''
    列出所有文章
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    文章的查询
    '''
    lookup_field = 'slug'
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        article.increase_views()
        return super().get(request, *args, **kwargs)


class ArticleCreate(generics.CreateAPIView):
    '''
    文章的创建

    * 只有管理员可以进行操作
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsAdminUserOrReadOnly, )

    def create(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class AboutDetail(generics.RetrieveAPIView):
    '''
    获取About的相关信息
    '''
    queryset = About.objects.all()
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        about = get_object_or_404(self.queryset, pk=1)
        return about.article


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)


class ImageUpload(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'uid'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)
