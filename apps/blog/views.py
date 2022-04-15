from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DetailView, View
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _

from apps.authentication.helpers import AuthorRequiredMixin
from apps.blog.models import Article
from apps.blog.forms import ArticleForm


class ArticlesListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published articles list."""

    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()


class DraftsListView(ArticlesListView):
    """Overriding the original implementation to call the drafts articles
    list."""

    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()

# Article Prelease
class ArticleCreatorView(View):
    message = _("You have started a new article.")

    def get(self, request, *args, **kwargs):
        Article(user=request.user).save()
        messages.success(self.request, self.message)
        return reverse("articles:edit_article", args=self.pk)

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
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect(reverse("articles:list"))


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