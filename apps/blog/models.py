from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from slugify import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import uuid

import codecs
from lnd_grpc import lnd_grpc

lnrpc = lnd_grpc.Client(
    lnd_dir = settings.LND_FOLDER,
    macaroon_path = settings.LND_MACAROON_FILE,
    tls_cert_path = settings.LND_TLS_CERT_FILE,
    network = settings.LND_NETWORK,
)

class ArticleQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P").order_by("-date_published")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D").order_by("-date_published")


class Article(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")))

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="articles",
        on_delete=models.SET_NULL,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, null=True, unique=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = models.CharField(_("Content"), max_length=10000, blank=True)
    edited = models.BooleanField(default=False)
    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-date_published",)

    def __str__(self):
        return self.title

    def get_absolute_url(self): 
        return reverse('article', kwargs=[str(self.uuid)])

    def generate_pub_invoice(self):

        add_invoice_resp = lnrpc.add_invoice(value=settings.MIN_VIEW_AMOUNT, memo=self.title)
        r_hash_base64 = codecs.encode(add_invoice_resp.r_hash, 'base64')
        r_hash = r_hash_base64.decode('utf-8')
        payment_request = add_invoice_resp.payment_request

        from apps.payments.models import Payment
        payment = Payment.objects.create(user=self.user, article=self, purpose=Payment.PUBLISH, satoshi_amount=settings.MIN_PUBLISH_AMOUNT, r_hash=r_hash, payment_request=payment_request, status='pending_payment')
        payment.save()

    def get_view_count(self):
        return self.payments.filter(status="complete", purpose="view").count()