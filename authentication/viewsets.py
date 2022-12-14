from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

from .serializers import EmployeeRegistrationSerializer, LoginSerializer, EmptySerializer, ChangePasswordSerializer


class AuthViewset(ModelViewSet):
    queryset = []

    def get_permissions(self):
        if self.action in ['employee_registration', 'login_view']:
            self.permission_classes = [AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'employee_registration':
            return EmployeeRegistrationSerializer
        elif self.action == 'login_view':
            return LoginSerializer
        elif self.action == 'logout':
            return EmptySerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return EmptySerializer

    def list(self, request):
        return Response({
            "Employee Registration": f"{request.build_absolute_uri()}employee_registration/",
            "User Login": f"{request.build_absolute_uri()}login/",
            "Logout": f"{request.build_absolute_uri()}logout/",
            "change_password": f"{request.build_absolute_uri()}change_password/",
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
        send_mail(
            'Subject here',
            'Here is the message.',
            'rafsantestmail@gmail.com ',
            ['rafsanpust255@gmail.com'],
            fail_silently=False,
        )
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

    @action(detail=False, methods=['POST'], name='change_password', url_path='change_password')
    def change_password(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data, context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'password changed'}, status=status.HTTP_200_OK)
        return Response({'message': 'Please Login first'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
