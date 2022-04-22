"""paywalled URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView, TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.apps import apps
from apps.authentication import views as auth_views
from apps.blog import views as blog_views
from apps.core import views as core_views
from django.contrib.sitemaps.views import sitemap
from django.views import defaults as default_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("", include("django.contrib.auth.urls")),
    path("login/success/", core_views.LoginRedirectView.as_view(), name="login_redirect"),
    path("signup/", auth_views.SignUpView.as_view(), name="signup"),
    path("signin/", RedirectView.as_view(pattern_name="login"), name="signin"),
    path("articles/", include("apps.blog.urls", namespace="articles")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
    path('admin/', admin.site.urls),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("settings/", include("apps.accounts.urls", namespace="settings")),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development
    urlpatterns += [
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns 