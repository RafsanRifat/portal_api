from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.viewsets import EmployeesViewset

router = DefaultRouter()
router.register(r'employees', EmployeesViewset, basename="employees")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
