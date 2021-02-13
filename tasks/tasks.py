from celery import shared_task

from django.core.mail import send_mail

from django.conf import settings
from .models import Task

from mytodolist.celery import app

'''
from time import sleep


@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_email_task():
    sleep(10)
    subject = 'HELLO FROM DJANGO!!!'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['wowoc24880@poetred.com',]
    send_mail( subject, message, email_from, recipient_list, fail_silently = False )
    
'''

@app.task
def query_every_min():
    tasks = Task.objects.all()
    for task in tasks:
        if task.finishes_in_10_minutes == True:
            user_email = task.author.email
            if user_email:
                subject = task.title
                message = ' Hurry up. Just 10 minutes to complete'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_email,]
                send_mail( subject, message, email_from, recipient_list, fail_silently = False )
    