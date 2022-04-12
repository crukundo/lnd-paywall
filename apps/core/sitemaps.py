from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Entry


class StaticSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["home", "about", "blog:entries"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(status=Entry.PUBLISHED).order_by("-start_publication")

    def lastmod(self, obj):
        return obj.last_update