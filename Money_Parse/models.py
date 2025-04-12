from django.db import models
import datetime

# Create your models here.
class Transaction(models.Model): #blueprint for the transactions database
    # Sets up relationship between transaction and user; if user is deleted, so are their transacatins
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #defines database to include category, name, amount, and date fields
    category = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()
    transaction_number = models.CharField(max_length = 20, unique = True, blank = True) # shouldnt blank be false

    #saves the transaction number when transaction object is created.
    def save(self, *args, **kwargs):
        if not self.transaction_number:
            self.transaction_number = f"T{datetime.datetime.now.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs) #call parent class to save to the database

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.category} - {self.name} - ${self.amount} - {self.date} "
