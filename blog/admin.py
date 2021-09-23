from django.contrib import admin

from .models import Article, Category, About

admin.site.register([Article, Category, About])
