from rest_framework import serializers
from .models import Transaction, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'transaction',
            'payment_method',
            'payment_status',
            'payment_timestamp'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(
        many=True, read_only=True, source='payment_set')

    class Meta:
        model = Transaction
        fields = [
            'id',
            'buyer',
            'seller',
            'credit',
            'quantity',
            'total_price',
            'transaction_status',
            'timestamp',
            'payments'
        ]
