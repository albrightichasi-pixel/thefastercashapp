from django.db import models
from django.conf import settings
from investments.models import Investment

User = settings.AUTH_USER_MODEL


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, null=True, blank=True)

    phone_number = models.CharField(max_length=15)
    amount = models.FloatField()

    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_desc = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, default='PENDING')  # PENDING, SUCCESS, FAILED

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
