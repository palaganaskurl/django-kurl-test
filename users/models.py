from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager
from users.tokens import AccountActivationTokenGenerator


class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_active = models.BooleanField(_("is active"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def email_user(self):
        email_html = render_to_string('activate_email.html', {
            'email': self.email,
            'domain': settings.ACTIVATION_URL,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': AccountActivationTokenGenerator().make_token(self),
        })
        plain_message = strip_tags(email_html)

        send_mail(
            'Activate your account',
            plain_message,
            'no-reply@sample.com',
            [self.email],
            fail_silently=False,
            html_message=email_html
        )
