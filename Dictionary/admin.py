from django.contrib import admin
from .models import Word, User, Category

admin.site.register(Word)
admin.site.register(Category)
admin.site.register(User)