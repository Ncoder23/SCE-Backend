from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SustainabilityCreditViewSet, UserCreditViewSet

router = DefaultRouter()
router.register(r'sustainability-credits',
                SustainabilityCreditViewSet, basename='sustainability-credit')
router.register(r'user-credits', UserCreditViewSet, basename='user-credit')

urlpatterns = [
    path('', include(router.urls)),
]
