import os.path

from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from apps.blog.models import Entry


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    public_email = models.EmailField(_("public email"), blank=True)
    location = models.CharField(_("location"), max_length=50, blank=True)
    url = models.CharField(_("url"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        db_table = "auth_profile"

    def __str__(self):
        return self.get_screen_name()

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url

    def get_picture(self):
        no_picture = django_settings.STATIC_URL + "img/user.png"
        try:
            filename = f"{django_settings.MEDIA_ROOT}/profile_pictures/{self.user.username}.jpg"
            picture_url = f"{django_settings.MEDIA_URL}profile_pictures/{self.user.username}.jpg"
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except Exception:
            return self.user.username

    def get_blogs(self):
        user_blogs = []
        author_blogs = Entry.objects.select_related("author__profile").filter(author=self.user)
        for r in author_blogs:
            user_blogs.append(r)
        user_blogs.sort(key=lambda r: r.last_update, reverse=True)
        return user_blogs


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)