from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.viewsets import EmployeesPublicViewset
from authentication.viewsets import AuthViewset

router = DefaultRouter()
router.register(r'public_employees', EmployeesPublicViewset, basename="public_employees")
router.register(r'auth', AuthViewset, basename="auth")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
