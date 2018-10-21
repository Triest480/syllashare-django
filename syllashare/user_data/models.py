from django.db import models


# Create your models here.


# | ID | SCHOOL NAME | CITY | STATE |
class School(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=16)


# | ID | EVENT TYPE |
class EventType(models.Model):
    event_type = models.CharField(max_length=32)


# | ID | SCHOOL | CLASS NAME | EVENT NAME | EVENT TYPE |
class SyllabusEvent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)  # if school is delete, do delete relevant entries
    class_name = models.CharField(max_length=256)
    entry_name = models.CharField(max_length=256)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)  # if event type is deleted kill corr. entries
    date = models.DateField()
    # TODO: Implement Time. (Right now can only handle day, month, year)


# | ID | FIRST NAME | LAST NAME | COGNITO USERNAME | EMAIL | SCHOOL |
class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128, null=True)

    # if school is somehow delete, don't delete user
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.SET_NULL)

    # implicit Many-to-Many Table Created
    syllabi = models.ManyToManyField(SyllabusEvent)


# | ID | TOKEN | DEVICE TYPE | USER |
class RefreshToken(models.Model):
    token = models.CharField(max_length=128)
    device_type = models.CharField(max_length=32)
    expiration_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
