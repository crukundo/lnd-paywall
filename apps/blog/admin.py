from django.contrib import admin
from apps.blog.models import Article


# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ("title", "user", "status")
#     list_filter = ("user", "status", "timestamp")


admin.site.register(Article)