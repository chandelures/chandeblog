from django.urls import re_path, path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('articles', views.ArticleList.as_view(), name='article-list'),

    re_path(r'^articles/(?P<slug>[-\w]+)$',
            views.ArticleDetail.as_view(), name='article-detail'),

    path('create/articles',
         views.ArticleCreate.as_view(), name='article-create'),

    path('categories', views.CategoryList.as_view(), name='category-list'),

    re_path(r'^categories/(?P<slug>[-\w]+)$',
            views.CategoryDetail.as_view(), name='category-detail'),

    path('create/categories', views.CategoryCreate.as_view(),
         name='category-create'),

    path('about', views.AboutDetail.as_view(), name='about'),
]
