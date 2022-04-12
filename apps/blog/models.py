from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from slugify import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class ArticleQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")


class Article(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="author",
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        _("Featured image"), upload_to="articles_pictures/%Y/%m/%d/"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = MarkdownxField()
    edited = models.BooleanField(default=False)
    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)