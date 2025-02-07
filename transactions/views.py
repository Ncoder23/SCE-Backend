from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Payment
from .serializers import TransactionSerializer, PaymentSerializer

# Create your views here.


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter transactions based on user role (buyer or seller)"""
        user = self.request.user
        return Transaction.objects.filter(
            buyer=user) | Transaction.objects.filter(seller=user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Custom endpoint to cancel a transaction"""
        transaction = self.get_object()
        if transaction.transaction_status == 'pending':
            transaction.transaction_status = 'cancelled'
            transaction.save()
            return Response({'status': 'transaction cancelled'})
        return Response(
            {'error': 'Cannot cancel transaction in current state'},
            status=status.HTTP_400_BAD_REQUEST
        )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter payments based on user's transactions"""
        user = self.request.user
        return Payment.objects.filter(
            transaction__buyer=user) | Payment.objects.filter(
            transaction__seller=user)

    def perform_create(self, serializer):
        """Add additional validation before creating payment"""
        transaction = serializer.validated_data['transaction']
        if transaction.transaction_status != 'pending':
            raise serializer.ValidationError(
                "Cannot add payment to non-pending transaction")
        serializer.save()
