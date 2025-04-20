from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    goals = models.TextField(blank=True)
    categories = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
