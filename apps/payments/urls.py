from django.urls import path
from apps.payments import views

app_name = "payments"

urlpatterns = [
    path('check_payment/<int:pk>/', views.check_payment, name="check-payment")
]