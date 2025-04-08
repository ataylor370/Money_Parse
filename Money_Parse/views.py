from .models import Transaction, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
def home(request):
     return render(request,'home.html',{})
def about(request):
     return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
# methods for transaction database modification
def create_transaction(request):
     if request.method == "POST":
          Transaction.objects.create(
               user = request.user,
               category = request.POST['category'],
               name = request.POST['name'],
               amount = request.POST['amount'],
               date = request.POST['date'],
          )
          #return methods set to the main screen transaction template
         return redirect("main_transaction_template") #shouldnt redirect anywhere if on main screen
def edit_transaction(request, transaction_number):
    transaction = get_object_or_404(Transaction, id = transaction_number)
    if request.method == "POST":
         transaction.category = request.POST['category']
         transaction.name = request.POST['name']
         transaction.amount = request.POST['amount']
         transaction.date = request.POST['date'] #note: although the date changes the transaction number wouldn't change

def delete_transaction(request, transaction_number):
     transaction = get_object_or_404(Transaction, id = transaction_number, user = request.user)
     if request.method == "POST":
          transaction.delete()
          return redirect("transactions_expanded") # expanded page for transactions

# methods for category database modification
def create_category(request):
     if request.method == "POST":
          Category.objects.create(
               name = request.POST['name'],
          )
def delete_category(request, category_name):
     category = get_object_or_404(Category, name = category_name)
     if request.method == "POST":
          category.delete()
          return redirect("budget_expanded") #expanded page for budget




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


