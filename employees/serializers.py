from rest_framework.serializers import ModelSerializer
from .models import EmployeesProfile


class EmployeesProfileSerializer(ModelSerializer):
    class Meta:
        model = EmployeesProfile
        fields = '__all__'
