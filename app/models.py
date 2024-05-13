from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


class Message(models.Model):
    user_from = models.ForeignKey(User, related_name='sender', on_delete=CASCADE)
    user_to = models.ForeignKey(User, related_name='receiver', on_delete=CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField()
