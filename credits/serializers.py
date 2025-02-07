from rest_framework import serializers
from .models import SustainabilityCredit, UserCredit


class SustainabilityCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SustainabilityCredit
        fields = '__all__'


class UserCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredit
        fields = '__all__'
