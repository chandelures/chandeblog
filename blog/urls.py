from django.urls import re_path, path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('articles', views.ArticleList.as_view(), name='article-list'),

    path('articles/create',
         views.ArticleCreate.as_view(), name='article-create'),

    re_path(r'^articles/(?P<slug>[-\w]+)$',
            views.ArticleDetail.as_view(), name='article-detail'),

    path('categories/create', views.CategoryCreate.as_view(),
         name='category-create'),

    path('categories', views.CategoryList.as_view(), name='category-list'),

    re_path(r'^categories/(?P<slug>[-\w]+)$',
            views.CategoryDetail.as_view(), name='category-detail'),

    path('about', views.AboutDetail.as_view(), name='about'),

    path('images/create', views.ImageUpload.as_view(), name='image-upload'),

    path('images', views.ImageList.as_view(), name='image-list'),

    re_path(r'^images/(?P<pk>[0-9]+)$',
            views.ImageDelete.as_view(), name='image-delete'),
]
