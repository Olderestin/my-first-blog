from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def sending_email_task(email_subject, message, to):
    email = EmailMessage(email_subject, message, to=to)
    try:
        email.send()
    except Exception as e:
        print('Error: {e}')
