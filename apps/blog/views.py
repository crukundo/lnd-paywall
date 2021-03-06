from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
        "drafts": drafts
    }
    return render(request, "blog/draft_list.html", context)

@login_required()
def list_articles(request):
    articles = request.user.articles.filter(status="P")
    context = {
        "articles": articles
    }
    return render(request, "blog/article_list.html", context)

@login_required()
def create_new_article(request):
    article = Article.objects.create(user=request.user)
    article.save()

    try:
        article.generate_pub_invoice()
    except:
        raise NotImplementedError()

    return redirect(reverse("articles:publish_article", kwargs={
        'article_uuid': article.uuid
    }))

@login_required()
def publish_new_article(request, article_uuid):

    article = request.user.articles.get(uuid=article_uuid)
    invoice = None
    payment_made = False

    try:
        # check existence of 'to publish' payments for this article and this user
        invoices = article.payments.filter(purpose='publish', user=request.user)
        if invoices:
            # we just need THE one
            invoice = invoices.first()
            if invoice.status == 'complete':
                payment_made = True
        else:
            # if no existing payment objects to view this article by this user
            article.generate_pub_invoice()
    except:
        raise NotImplementedError()

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        # Publish article after payment
        if form.is_valid():
            article = form.save(commit=False)
            if "publish" in request.POST:
                article.status = Article.PUBLISHED
                messages.success(request, "Your article: '{}' has been published successfully".format(article.title))

            elif "save" in request.POST:
                article.status = Article.DRAFT
                messages.success(request, "Draft: '{}' has been saved successfully".format(article.title))
            article.save()

            return redirect(reverse("home"))

    else:
        form = ArticleForm(instance=article)
    
    return render(request, "blog/publish_article.html", {
        'article': article,
        'form': form,
        'invoice': invoice,
        'payment_made': payment_made
    })

@login_required()
def delete_draft_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect(reverse("articles:drafts"))

@login_required()
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect(reverse("home"))


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
        return reverse("home")

def article_detail(request, article_uuid):
    article = Article.objects.get(uuid=article_uuid)
    # assume the worst first, lol
    payment_made = False
    received_payments = None
    invoice = None

    try:
        # create session key if non-existent
        if not request.session.session_key:
            request.session.create()
        # check if logged in user has a "to view" invoice and whether paid?
        if request.user.is_authenticated:
            invoices = article.payments.filter(purpose='view', user=request.user)
            if invoices:
                # we just need THE one
                invoice = invoices.last()
                if invoice.status == 'complete':
                    payment_made = True
                    # add session key to invoice
                    invoice.session_key = request.session.session_key
            else:
                article.generate_view_invoice()
                invoice = article.payments.filter(purpose='view').latest("created_at")
        else:
            # get the most recent "to view" invoice for this particular session
            invoices = article.payments.filter(purpose='view', session_key=request.session.session_key)
            if invoices:
                # we just need THE one
                invoice = invoices.last()
                if invoice.status == 'complete':
                    payment_made = True
                    # add session key to invoice
                    invoice.session_key = request.session.session_key
            else:
                article.generate_view_invoice()
                invoice = article.payments.latest("modified_at")
    except:
        raise NotImplementedError()

    received_payments = article.payments.filter(status='complete').order_by('-modified_at')

    return render(request, "blog/article_detail.html", {
        'article': article,
        'invoice': invoice,
        'payment_made': payment_made,
        'received_payments': received_payments
    })

# @todo: on edit, check if lightning publish invoice has expired and create a new one. Also mark payment as expired
