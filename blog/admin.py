from django.contrib import admin
from .models import *
from mdeditor.widgets import MDEditorWidget

admin.site.register([Post, Category, Column, ColumnCategory])
