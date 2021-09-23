from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api-root'),

    path('articles', views.ArticleList.as_view(), name='article-list'),

    path('articles/create',
         views.ArticleCreate.as_view(), name='article-create'),

    path('articles/<slug:slug>',
         views.ArticleDetail.as_view(), name='article-detail'),

    path('categories/create', views.CategoryCreate.as_view(),
         name='category-create'),

    path('categories', views.CategoryList.as_view(), name='category-list'),

    path('categories/<slug:slug>',
         views.CategoryDetail.as_view(), name='category-detail'),

    path('about', views.AboutDetail.as_view(), name='about'),

    path('images/create', views.ImageUpload.as_view(), name='image-upload'),

    path('images', views.ImageList.as_view(), name='image-list'),

    path('images/<uuid:uid>',
         views.ImageDetail.as_view(), name='image-delete'),
]
