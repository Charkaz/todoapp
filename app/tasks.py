from django.shortcuts import render,redirect,get_object_or_404
from celery import Celery
from .models import newtasks,serhs
import time
from django.core.mail import send_mail
from django.conf import settings

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x,y):

    return x+y

@app.task
def sendemail(subject,message,email_from,recipient_list):
    try:
        send_mail( subject, message, email_from, recipient_list )
    except:
        print("sehf bas verdi")