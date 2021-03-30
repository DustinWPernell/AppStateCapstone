from django.core.mail import send_mail


def send_password_reset(body, to):
    send_mail(
        'Nenniltoz Password Reset',
        body ,
        'dustin.w.pernell@gmail.com',
        to ,
        fail_silently=False,
    )