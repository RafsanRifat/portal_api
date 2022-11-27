from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.


class EmployeesProfile(models.Model):
    GENDER = [
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=8, choices=GENDER)
    avatar = models.ImageField('profile_pictures/employees', blank=True, null=True)
    phone_number = models.IntegerField(null=True)
    alternative_phone_number = models.IntegerField(null=True)
    skype = models.CharField(max_length=30, null=True)
    mailing_address = models.CharField(max_length=50, null=True)
    alternative_address = models.CharField(max_length=50, null=True)
    is_verified = models.BooleanField(default=False)
