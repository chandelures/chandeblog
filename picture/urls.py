from django.urls import path

from picture import views

app_name = 'picture'

urlpatterns = [
    path('create', views.ImageUpload.as_view(), name='image-upload'),

    path('', views.ImageList.as_view(), name='image-list'),

    path('<uuid:uid>',
         views.ImageDetail.as_view(), name='image-delete'),
]
