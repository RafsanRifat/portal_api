from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import EmployeeRegistrationSerializer


class AuthViewset(ModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'employee_registration':
            return EmployeeRegistrationSerializer

    @action(detail=False, methods=['POST'], name='employee registration', url_path='employee_registration')
    def employee_registration(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account has been created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
