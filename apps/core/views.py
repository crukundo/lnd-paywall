from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from apps.blog.models import Article
from apps.payments.models import Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home(request):
    published_articles = Article.objects.get_published()
    payments = Payment.objects.filter(status='complete').order_by('-modified_at')
    return render(
        request, "core/home.html", {
            "articles": published_articles,
            "payments": payments
        },
    )


class LoginRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("articles:list")