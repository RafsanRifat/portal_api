from django.core.serializers import get_serializer
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import EmployeesProfile
from rest_framework.response import Response

from .serializers import EmployeesProfileSerializer


class EmployeesPublicViewset(ModelViewSet):
    http_method_names = ['get']

    def get_queryset(self):
        return EmployeesProfile.objects.all()

    def get_serializer_class(self):
        return EmployeesProfileSerializer
