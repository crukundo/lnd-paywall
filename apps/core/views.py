from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from apps.blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    published_articles = Article.objects.filter(status=Article.PUBLISHED).order_by("-date_published")
    return render(
        request,
        "core/home.html",
        {"articles": published_articles},
    )


class LoginRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("articles:list")