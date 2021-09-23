from django.urls import path, include

from picture import views

app_name = 'picture'

urlpatterns = [
    path('/', include([
        path('create', views.ImageUpload.as_view(), name='image-upload'),
        path('<uuid:uid>',
         views.ImageDetail.as_view(), name='image-delete'),
    ])),

    path('', views.ImageList.as_view(), name='image-list'),
]
