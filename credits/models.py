# credits/models.py
from django.db import models
from users.models import CustomUser


class SustainabilityCredit(models.Model):
    CREDIT_TYPES = [
        ('carbon_credit', 'Carbon Credit'),
        ('REC', 'Renewable Energy Credit'),
        ('plastic_credit', 'Plastic Credit'),
    ]
    credit_type = models.CharField(max_length=20, choices=CREDIT_TYPES)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    origin_country = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.IntegerField()
    issued_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name} - {self.credit_type}"


class UserCredit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    credit = models.ForeignKey(SustainabilityCredit, on_delete=models.CASCADE)
    quantity_owned = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} owns {self.quantity_owned} of {self.credit}"
