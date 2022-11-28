from django.contrib import admin
from .models import EmployeesProfile, SocialLinks, EmployeeSocialLinks

# Register your models here.
admin.site.register(EmployeesProfile)
admin.site.register(SocialLinks)
admin.site.register(EmployeeSocialLinks)
