import re
from django.shortcuts import render, get_object_or_404
from apps.blog.models import Article
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django_htmx.http import HttpResponseStopPolling

from apps.payments.models import Payment

import codecs
from lnd_grpc import lnd_grpc

import lnd_grpc.protos.rpc_pb2 as ln

lnrpc = lnd_grpc.Client(
    lnd_dir = settings.LND_FOLDER,
    macaroon_path = settings.LND_MACAROON_FILE,
    tls_cert_path = settings.LND_TLS_CERT_FILE,
    network = settings.LND_NETWORK,
)


# Create your views here.

def check_payment(request, pk):
    """
    Checks if the Lightning payment has been received for this invoice
    """
    # get the payment in question
    payment = Payment.objects.get(pk=pk)

    r_hash_base64 = payment.r_hash.encode('utf-8')
    r_hash_bytes = codecs.decode(r_hash_base64, 'base64')
    invoice_resp = lnrpc.lookup_invoice(r_hash=r_hash_bytes)


    if request.htmx:
        if invoice_resp.settled:
            # Payment complete
            payment.status = 'complete'
            if request.user.is_authenticated:
                payment.user = request.user
            payment.save()
            return HttpResponseStopPolling("<div id='paymentStatus' data-status='paid' class='alert alert-success' role='alert'>Payment confirmed. Thank you</div>")
        else:
            # Payment not received
            return HttpResponse("<div id='paymentStatus' data-status='pending' class='alert alert-warning' role='alert'>Invoice payment is still pending. Will check again in 10s</div>")

        