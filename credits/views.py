from rest_framework import viewsets
from .models import SustainabilityCredit, UserCredit
from .serializers import SustainabilityCreditSerializer, UserCreditSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class SustainabilityCreditViewSet(viewsets.ModelViewSet):
    serializer_class = SustainabilityCreditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SustainabilityCredit.objects.all()


class UserCreditViewSet(viewsets.ModelViewSet):
    serializer_class = UserCreditSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCredit.objects.filter(user=self.request.user)
