from django.db import models


# | ID | SCHOOL NAME | CITY | STATE |
class School(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=16)
    pic_key = models.CharField(max_length=200)


# | ID | DEPARTMENT_NAME |
class Department(models.Model):
    department_name = models.CharField(max_length=256)


# | ID | TERM |
class Term(models.Model):
    term = models.CharField(max_length=8)  # FALL, WINTER, SPRING, SUMMER


# | ID | EVENT TYPE |
class EventType(models.Model):
    event_type = models.CharField(max_length=32)  # midterm, homework, final, event, etc


# | ID | FIRST NAME | LAST NAME | DEPARTMENT | SCHOOL | RATING | WEBSITE |
class Teacher(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    rating = models.FloatField(null=True)
    website = models.URLField(null=True)


# | ID | CLASS_NAME | SCHOOL | TEACHER | TERM | YEAR | SYLLABUS_EVENTS |
class Class(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_number = models.CharField(max_length=256)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, null=True, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)


# | ID | CLASS | EVENT NAME | EVENT TYPE | DATE |
class SyllabusEvent(models.Model):
    class_from = models.ForeignKey(Class, on_delete=models.CASCADE)
    entry_name = models.CharField(max_length=256)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)  # if event type is deleted kill corr. entries
    date = models.DateField()
    # TODO: Implement Time. (Right now can only handle day, month, year)


# | ID | FIRST NAME | LAST NAME | COGNITO USERNAME | EMAIL | SCHOOL |
class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.CharField(max_length=128, null=True)
    pic_key = models.CharField(max_length=200, null=True)
    # if school is somehow deleted, don't delete user
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.SET_NULL)

    # implicit Many-to-Many Table Created
    classes = models.ManyToManyField(Class)
