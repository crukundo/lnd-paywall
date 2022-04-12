from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.SettingsRedirectView.as_view(), name="settings"),
    path("profile/", views.UpdateProfileView.as_view(), name="profile"),
    path("emails/", views.UpdateEmailsView.as_view(), name="emails"),
]