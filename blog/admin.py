from django.contrib import admin

from .models import Article, Category, About, Image

admin.site.register([Article, Category, About, Image])
