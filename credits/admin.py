from django.contrib import admin

# Register your models here.
from .models import SustainabilityCredit, UserCredit

admin.site.register(SustainabilityCredit)
admin.site.register(UserCredit)
