from django.db import models
from django.contrib.auth.models import Group, User
from PIL import Image


# Create your models here.

class SocialLinks(models.Model):
    name = models.CharField(max_length=15)
    link = models.URLField()

    def __str__(self):
        return self.name


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
    sociallinks = models.ManyToManyField(SocialLinks, through='EmployeeSocialLinks')

    # Compressing image before saving in Database
    def save(self, *args, **kwargs):
        if self.avatar:
            image = Image.open(self.avatar)
            image = image.resize((300,300))
            image.save(self.avatar.path, optimize=True, quality=85)
        super(EmployeesProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class EmployeeSocialLinks(models.Model):
    employeeprofile = models.ForeignKey(EmployeesProfile, on_delete=models.CASCADE)
    sociallinks = models.ForeignKey(SocialLinks, on_delete=models.CASCADE)
    link = models.URLField(blank=True, null=True)
    show_hide = models.BooleanField(default=False)

    def __str__(self):
        return self.sociallinks.name
