from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.viewsets import EmployeesPublicViewset

router = DefaultRouter()
router.register(r'public_employees', EmployeesPublicViewset, basename="public_employees")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
