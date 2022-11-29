from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import EmployeeRegistrationSerializer, LoginSerializer


class AuthViewset(ModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'employee_registration':
            return EmployeeRegistrationSerializer
        elif self.action == 'login_view':
            return LoginSerializer

    @action(detail=False, methods=['POST'], name='employee registration', url_path='employee_registration')
    def employee_registration(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account has been created successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], name='user login', url_path='login')
    def login_view(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
