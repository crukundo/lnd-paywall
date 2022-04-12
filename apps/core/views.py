from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from apps.blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user_blogs = Article.objects.filter(status=Article.PUBLISHED).order_by("-timestamp")
        latest_blog = Article.objects.filter(status=Article.PUBLISHED).order_by("-timestamp").first()
        return render(
            request,
            "core/home.html",
            {"user_blogs": user_blogs, "latest_blog": latest_blog},
        )
    return render(request, "core/cover.html")


class LoginRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("blog", kwargs={"username": self.request.user.username})