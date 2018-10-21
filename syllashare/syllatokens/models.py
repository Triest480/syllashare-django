from django.db import models
from user_data.models import User


# | ID | SYLLASHARE_TOKEN_STRING | USER | EXPIRATION_DATE |
class SyllaShareToken(models.Model):
    syllashare_token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()
