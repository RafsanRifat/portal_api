from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import EmployeeRegistrationSerializer, LoginSerializer, EmptySerializer


class AuthViewset(ModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'employee_registration':
            return EmployeeRegistrationSerializer
        elif self.action == 'login_view':
            return LoginSerializer
        elif self.action == 'logout':
            return EmptySerializer
        return EmptySerializer

    def list(self, request):
        return Response({
            "Employee Registration": f"{request.build_absolute_uri()}employee_registration/",
            "User Login": f"{request.build_absolute_uri()}login/",
            "Logout": f"{request.build_absolute_uri()}logout/",
        })

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

    @action(detail=False, methods=['POST'], name='logout', url_path='logout')
    def logout(self, request):
        # getting all the tokens of the current user
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        # blacklisting all the tokens of the current user
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
