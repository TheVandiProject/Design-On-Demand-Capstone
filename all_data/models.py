from django.db import models

# Create your models here.
class Users(models.Model):
    email_address = models.EmailField(unique = True, max_length=100)
    username = models.CharField(unique = True, max_length=100)
    password = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)