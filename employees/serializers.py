from rest_framework.serializers import ModelSerializer
from .models import EmployeesProfile, EmployeeSocialLinks, SocialLinks


class EmployeeSocialLinksSerializer(ModelSerializer):
    class Meta:
        model = EmployeeSocialLinks
        fields = '__all__'


class SocialLinksSerializer(ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = '__all__'


class EmployeesProfileSerializer(ModelSerializer):
    sociallinks = SocialLinksSerializer

    class Meta:
        model = EmployeesProfile
        fields = '__all__'
