from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, UpdateView, DetailView, View
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _

from apps.authentication.helpers import AuthorRequiredMixin
from apps.blog.models import Article
from apps.blog.forms import ArticleForm


@login_required()
def list_drafts(request):
    drafts = request.user.articles.filter(status="D")
    context = {
        "articles": drafts
    }
    return render(request, "blog/draft_list.html", context)

@login_required()
def list_articles(request):
    articles = Article.objects.get_published()
    context = {
        "articles": articles
    }
    return render(request, "blog/article_list.html", context)

@login_required()
def create_new_article(request):
    article = Article.objects.create(user=request.user)
    article.save()
    return redirect(reverse("articles:publish_article", kwargs={'article_uuid': article.uuid}))

@login_required()
def publish_new_article(request, article_uuid):
    article = get_object_or_404(Article, uuid=article_uuid)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            print('valid')
            article = form.save(commit=False)
            article.status = Article.PUBLISHED
            article.save()
            messages.success(request, "Article: '{}' has been published successfully".format(article.title))
            return redirect(reverse("articles:list"))

    else:
        form = ArticleForm(instance=article)
    
    return render(request, "blog/publish_article.html", {
        'article': article,
        'form': form
    })

@login_required()
@require_http_methods(['DELETE'])
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    articles = Article.objects.all()
    # return redirect(reverse("articles:list"))
    return render(request, "blog/article_list.html", {
        'articles': articles
    })


class CreateArticleView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""

    model = Article
    message = _("Your article has been created.")
    form_class = ArticleForm
    template_name = "blog/create_article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:list")


class EditArticleView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing articles."""

    model = Article
    message = _("Your article has been updated.")
    form_class = ArticleForm
    template_name = "blog/update_article.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("articles:list")


class DetailArticleView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual article."""

    model = Article

    def get_object(self, queryset=None):
        return Article.objects.get(uuid=self.kwargs.get("uuid"))