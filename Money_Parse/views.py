from django.shortcuts import render
import datetime
def home(request):
     return render(request,'home.html',{})
def about(request):
     return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
# Create your views here.
class transaction:
     def __init__(self, category, name, amount, date, transaction_number):
          self.category = category
          self.name = name
          self.amount = amount
          self.date = date
          self.transaction_number = f"T{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
     def __repr__(self):
          return f"Transaction(transaction_number={self.transaction_number}, category='{self.category}', amount={self.amount})" #Not sure where use case for string representation is yet but its here just in case

class transaction_manager:
     def __init__(self):
          self.transactions = []
     def create_transaction(self, category, name, amount, date, transaction_number):
          self.transactions.append(transaction(category, name, amount, date, transaction_number)) #line fix to add new transaction to database
     def delete_transaction(self, transaction_number):
          for transaction in self.transactions:
              if transaction.transaction_number == transaction_number:
                   self.transactions.remove(transaction)
     def edit_transaction(self, new_category, new_name, new_amount, new_date, transaction_number):
          for transaction in self.transactions:
               if transaction.transaction_number == transaction_number:
                    transaction.category = new_category
                    transaction.name = new_name
                    transaction.amount = new_amount
                    transaction.date = new_date
     def get_tranasactions(self):
          return self.transactions

class category:
     def __init__(self, name):
          self.name = name
     def __repr__(self):
          return f"Category(name={self.name})" #Not sure where use case for string representation is yet but its here just in case


class category_manager:
     def __init__(self):
          self.categories = []
     def create_category(self, name):
          self.categories.append(category(name))
     def delete_category(self, name):
          for category in self.categories:
               if category.name == name:
                    self.categories.remove(category)


