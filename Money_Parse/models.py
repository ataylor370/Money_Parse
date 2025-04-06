from django.db import models

# Create your models here.
# app/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - ${self.amount}"
