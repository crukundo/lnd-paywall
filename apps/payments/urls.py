from django.urls import path
from apps.payments import views

app_name = "payments"

urlpatterns = [
    path('gen_pub_invoice/<uuid:uuid>', views.generate_pub_invoice, name="generate_pub_invoice")
]