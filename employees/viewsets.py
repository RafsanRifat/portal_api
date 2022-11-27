from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import EmployeesProfile
from rest_framework.response import Response

from .serializers import EmployeesProfileSerializer


class EmployeesViewset(ModelViewSet):

    def get_queryset(self):
        if self.action == 'employees':
            return EmployeesProfile.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'employees':
            return EmployeesProfileSerializer

    @action(detail=False, methods=['Get'], name='employees', url_path='employees')
    def employees(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
