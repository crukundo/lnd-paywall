from django.db import models
from django.conf import settings
from apps.blog.models import Article    

import codecs
from lnd_grpc import lnd_grpc

from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.contrib.sessions.models import Session

import lnd_grpc.protos.rpc_pb2 as ln

lnrpc = lnd_grpc.Client(
    lnd_dir = settings.LND_FOLDER,
    macaroon_path = settings.LND_MACAROON_FILE,
    tls_cert_path = settings.LND_TLS_CERT_FILE,
    network = settings.LND_NETWORK,
)

# Create your models here.

class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ('pending_invoice', 'Pending Invoice'), # Should be atomic
        ('pending_payment', 'Pending Payment'),
        ('complete', 'Complete'),
        ('error', 'Error'),
    )

    PUBLISH = "publish"
    VIEW = "view"
    EDIT = "edit"
    COMMENT = "comment"
    PAYMENT_PURPOSE_CHOICES = (
        (PUBLISH, 'Publish'),
        (VIEW, 'View'),
        (EDIT, 'Edit'),
        (COMMENT, 'Comment'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="payments",
        on_delete=models.SET_NULL,
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='payments')
    purpose = models.CharField(max_length=10, choices=PAYMENT_PURPOSE_CHOICES)

    satoshi_amount = models.IntegerField()
    r_hash = models.CharField(max_length=64)
    payment_request = models.CharField(max_length=1000)

    status = models.CharField(max_length=50, default='pending_invoice', choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def check_payment(self):
        """
        Checks if the Lightning payment has been received for this invoice
        """
        # if self.status == 'pending_payment':
        #     return False

        r_hash_base64 = self.r_hash.encode('utf-8')
        r_hash_bytes = str(codecs.decode(r_hash_base64, 'base64'))
        invoice_resp = lnrpc.lookup_invoice(ln.PaymentHash(r_hash=r_hash_bytes))

        if invoice_resp.settled:
            # Payment complete
            self.status = 'complete'
            self.save()
            return HttpResponse("Invoice paid successfully")
        else:
            # Payment not received
            return HttpResponse("Invoice pending payment")