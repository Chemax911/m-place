import os

from django.contrib.sites.shortcuts import get_current_site
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator


def send_email_for_verify(request, user):
    current_site = get_current_site(request)

    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }

    subject = render_to_string('registration/message_subject.txt', context).strip()
    text_message = render_to_string('registration/message.txt', context)
    html_message = render_to_string('registration/message.html', context)

    email_message = EmailMultiAlternatives(subject, text_message, to=[user.email])
    email_message.attach_alternative(html_message, 'text/html')
    img_dir = 'static'
    image = 'assets/images/demos/demo2/header-logo.png'
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as imgs:
        img = MIMEImage(imgs.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    email_message.attach(img)
    email_message.send()
