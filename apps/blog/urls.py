from django.conf.urls import url
from django.urls import path
from requests import delete

from apps.blog.views import (
    EditArticleView,
    DetailArticleView,
    list_drafts,
    list_articles,
    create_new_article,
    publish_new_article,
    delete_article,
    delete_draft_article
)

app_name = "articles"
urlpatterns = [
    path("", view=list_articles, name="list"),
    path("new/", view=create_new_article, name="write_new"),
    path("publish/<uuid:article_uuid>/", view=publish_new_article, name="publish_article"),
    path("drafts/", view=list_drafts, name="drafts"),
    path("edit/<int:pk>/", EditArticleView.as_view(), name="edit_article"),
    path("delete/<int:pk>/", view=delete_article, name="delete_article"),
    path("delete_draft/<int:pk>/", view=delete_draft_article, name="delete_draft"),
    path("<uuid:uuid>/", DetailArticleView.as_view(), name="article"),
]