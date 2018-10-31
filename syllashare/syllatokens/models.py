from django.db import models
from user_data.models import User


# | ID | SYLLASHARE_TOKEN_STRING | USER | EXPIRATION_DATE |
class SyllaShareToken(models.Model):
    syllashare_token = models.CharField(max_length=200)
    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()


# | ID | USER | ACCESS_TOKEN | REFRESH_TOKEN | PROVIDER | EXPIRATION DATE
class ServiceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    provider = models.CharField(max_length=50)
    expiration_date = models.DateTimeField()

    class Meta:
        unique_together = ("user", "provider")
