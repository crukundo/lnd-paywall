import re
from django.shortcuts import render, get_object_or_404
from apps.blog.models import Article
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpRequest, HttpResponse


# Create your views here.

@require_GET
def generate_pub_invoice(request: HttpRequest, uuid) -> HttpResponse:
    article = get_object_or_404(Article, uuid=uuid)
    # generate publishing invoice
    invoice = article.generate_pub_invoice()
    context = {'invoice': invoice }
    return render(request, 'partials/partial_invoice.html', context)