from django.db import models

# Create your models here.
class Users(models.Model):
    email_address = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)