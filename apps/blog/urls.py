from django.conf.urls import url
from django.urls import path
from requests import delete

from apps.blog.views import (
    ArticlesListView,
    DraftsListView,
    ArticleCreatorView,
    CreateArticleView,
    EditArticleView,
    DetailArticleView,
    create_new_article,
    publish_new_article,
    delete_article
)

app_name = "articles"
urlpatterns = [
    url(r"^$", ArticlesListView.as_view(), name="list"),
    url(r"^write-new-article/$", view=create_new_article, name="write_new"),
    path("publish/<uuid:article_uuid>/", view=publish_new_article, name="publish_article"),
    url(r"^drafts/$", DraftsListView.as_view(), name="drafts"),
    path("edit/<int:pk>/", EditArticleView.as_view(), name="edit_article"),
    path("delete/<int:pk>/", view=delete_article, name="delete_article"),
    url(r"^(?P<uuid>[-\w]+)/$", DetailArticleView.as_view(), name="article"),
]