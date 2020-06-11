
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from .tokens import account_token

def sendRegisterConfirmationMail(request, user):
    domain = get_current_site(request).domain
    mail_subject = 'Tournament Portal account activation'
    message = render_to_string('users/mails/registerConfirmation.html', {
        'name': user.first_name,
        'domain': domain,
        'uuid': urlsafe_base64_encode(force_bytes(user.uuid)),
        'token': account_token.make_token(user)
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send(fail_silently=False)

def sendPasswordResetMail(request, user):
    domain = get_current_site(request).domain
    mail_subject = 'Tournament Portal password reset'
    message = render_to_string('users/mails/passwordReset.html', {
        'name': user.first_name,
        'domain': domain,
        'uuid': urlsafe_base64_encode(force_bytes(user.uuid)),
        'token': account_token.make_token(user)
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send(fail_silently=False)