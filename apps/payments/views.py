import re
from django.shortcuts import render, get_object_or_404
from apps.blog.models import Article

# Create your views here.

def generate_pub_invoice(request, uuid):
    article = get_object_or_404(Article, uuid=uuid)
    # generate publishing invoice
    article.generate_pub_invoice()
    context = {'article': article }
    return render(request, 'partials/partial_invoice.html', context)