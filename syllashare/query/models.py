from django.db import models

# Create your models here.
class profile(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128)
    profilePicUrl = models.CharField(max_length=128)
