from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from api.routes import PatientViewSet, StudyViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")

patient_router = routers.NestedSimpleRouter(router, r"patients", lookup="patient")
patient_router.register(r"studies", StudyViewSet, basename="studies")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(patient_router.urls)),
]
