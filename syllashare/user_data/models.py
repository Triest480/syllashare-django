from django.db import models


# | PK | SCHOOL NAME | CITY | STATE |
class School(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=16)
    pic_key = models.CharField(max_length=200)


# | PK | DEPARTMENT_NAME |
class Department(models.Model):
    department_name = models.CharField(max_length=256)


# | PK | TERM |
class Term(models.Model):
    term = models.CharField(max_length=8)  # FALL, WINTER, SPRING, SUMMER


# | PK | EVENT TYPE |
class EventType(models.Model):
    event_type = models.CharField(max_length=32)  # midterm, homework, final, event, etc


# | PK | FIRST NAME | LAST NAME | DEPARTMENT | SCHOOL | RATING | WEBSITE |
class Teacher(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    rating = models.FloatField(null=True)
    website = models.URLField(null=True)


# | PK | CLASS_NAME | SCHOOL | TEACHER | TERM | YEAR | SYLLABUS_EVENTS |
class Class(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_description = models.CharField(max_length=256, default='')
    class_number = models.CharField(max_length=64)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    term = models.ForeignKey(Term, null=True, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)


# | PK | GROUP_NAME |
class Group(models.Model):
    group_name = models.CharField(max_length=256)


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
    groups = models.ManyToManyField(Group)


# | PK | CLASS | EVENT NAME | EVENT TYPE | DATE |
class SyllabusEvent(models.Model):
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    from_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_name = models.CharField(max_length=256)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)  # if event type is deleted kill corr. entries
    date = models.DateTimeField()
