from django.urls import path, include

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api-root'),

    path('articles', views.ArticleList.as_view(), name='article-list'),

    path('articles/', include([
        path('create',
         views.ArticleCreate.as_view(), name='article-create'),
        path('<slug:slug>',
         views.ArticleDetail.as_view(), name='article-detail'),
    ])),

    path('categories', views.CategoryList.as_view(), name='category-list'),

    path('categories/', include([
        path('create', views.CategoryCreate.as_view(),
             name='category-create'),
        path('<slug:slug>', views.CategoryDetail.as_view(),
             name='category-detail'),
    ])),

    path('about', views.AboutDetail.as_view(), name='about'),
]
