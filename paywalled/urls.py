"""paywalled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from django.conf import settings
from django.apps import apps
from apps.authentication import views as auth_views
from apps.core.sitemaps import BlogSitemap
from apps.blog import views as blog_views
from apps.core import views as core_views
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    "blog": BlogSitemap()
}

urlpatterns = [
    path("", core_views.home, name="home"),
    path("", include("django.contrib.auth.urls")),
    path("login/success/", core_views.LoginRedirectView.as_view(), name="login_redirect"),
    path("signup/", auth_views.SignUpView.as_view(), name="signup"),
    path("signin/", RedirectView.as_view(pattern_name="login"), name="signin"),
    path("blog/", include("apps.blog.urls", namespace="blog")),
    path('admin/', admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:

    if apps.is_installed("debug_toolbar"):
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    if apps.is_installed("silk"):

        urlpatterns = [path("__silk__/", include("silk.urls"))] + urlpatterns

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)