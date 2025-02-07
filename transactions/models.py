# transactions/models.py
from django.db import models
from users.models import CustomUser
from credits.models import SustainabilityCredit


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    buyer = models.ForeignKey(
        CustomUser, related_name='buyer_transactions', on_delete=models.CASCADE)
    seller = models.ForeignKey(
        CustomUser, related_name='seller_transactions', on_delete=models.CASCADE)
    credit = models.ForeignKey(SustainabilityCredit, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.buyer} -> {self.seller} ({self.quantity})"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('crypto', 'Crypto'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.transaction} ({self.payment_method})"
