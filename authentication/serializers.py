from django.contrib.auth.models import User, Group

from employees.models import EmployeesProfile
from rest_framework import serializers

from django.contrib import admin
from rest_framework.serializers import ModelSerializer


# Register your models here.

class EmployeeRegistrationSerializer(ModelSerializer):
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = EmployeesProfile
        fields = ('first_name', 'last_name', 'email', 'password', 'gender', 'phone_number',)

    def create(self, validated_data):
        user = User.objects.create(
            is_active=False,
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        try:
            new_group = Group.objects.get(name='Employees')
            user.groups.add(new_group)
        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Employees')
            user.groups.add(new_group)

        employees_profile = EmployeesProfile.objects.create(
            user=user,
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number']

        )
        employees_profile.save()
        return employees_profile


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if not user.check_password(attrs['password']):
                raise Exception('Wrong Password !')
        except Exception:
            raise serializers.ValidationError({"validation_error": "Email or password is incorrect"})
        return attrs


class EmptySerializer(serializers.Serializer):
    pass
