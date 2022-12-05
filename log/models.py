from django.db import models
from django.contrib.auth.models import User

class Speak(models.Model):
    txt = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    username = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.username