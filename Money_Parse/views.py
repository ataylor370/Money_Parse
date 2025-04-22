from .models import Transaction, Category, Exspenses, Goal, Income
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
import json
def home(request):
     return render(request,'home.html',{})
def about(request):
    request.user = None
    return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
def budget(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    goals = Goal.objects.filter(user=user)
    exspenses = Exspenses.objects.filter(user=user)
    #formatting the data for google charts api
    chart_data = [['Category', 'Amount']]
    for exspense in exspenses:
        chart_data.append([exspense.expense, exspense.amount])
    return render(request, 'Budget.html', {'categories': categories, 'goals': goals, 'chart_data': json.dumps(chart_data)})

def dashboard(request):
    user = request.user
    categories = Category.objects.filter(user = user)
    transactions = Transaction.objects.filter(user = user).order_by('-date')

    category_data = []
    for cat in categories:
        category_data.append({
            'name': cat.name,
            'budget': cat.budget,
            'spent': cat.spent,
        })

    return render(request, 'dashboard.html', {
        'categories': categories,
        'transactions': transactions,
        'category_data': category_data,
    })

# methods for transaction database modification
@login_required
def create_transaction(request):
    if request.method == "POST":
        # Create the transaction only if the method is POST
        Transaction.objects.create(
            user=request.user,
            category=get_object_or_404(Category, id=request.POST['category'], user=request.user),
            name=request.POST['name'],
            amount=request.POST['amount'],
        )

    # Always redirect to the dashboard after handling the POST request or just accessing the page
    return redirect('dashboard')

def edit_transaction(request, transaction_number):
    transaction = get_object_or_404(Transaction, id = transaction_number, user = request.user)
    if request.method == "POST":
         transaction.category = request.POST['category']
         transaction.name = request.POST['name']
         transaction.amount = request.POST['amount']
         transaction.date = request.POST['date'] #note: although the date changes the transaction number wouldn't change
def delete_transaction(request, transaction_number):
     transaction = get_object_or_404(Transaction, id = transaction_number, user = request.user)
     if request.method == "POST":
          transaction.delete()

# methods for category database modification
def create_category(request):
     if request.method == "POST":
          Category.objects.create(
              user = request.user,
              name = request.POST['name'],
          )
def delete_category(request, category_name):
     category = get_object_or_404(Category, name = category_name, user = request.user)
     if request.method == "POST":
          category.delete()

# methods for Goal database modification
def create_goal(request, new_goal):
    if request.method == "POST":
        Goal.objects.create(
            user = request.user,
            goal = new_goal,
        )
def edit_goal(request, goal_number):
    goal = get_object_or_404(Goal, id=goal_number, user=request.user)
    if request.method == "POST":
        goal.goal = request.POST['goal']
def delete_goal(request, goal_number):
    goal = get_object_or_404(Goal, id = goal_number, user = request.user)
    if request.method == "POST":
        goal.delete()
    # renumbering goals after deletion made
    remaining_goals = Goal.objects.filter(user=request.user).order_by('goal_number')
    for idx, goal in enumerate(remaining_goals, start=1):
        goal.goal_number = idx
        goal.save()


# methods for exspense database modification
def create_exspense(request, exspense, amount):
    if request.method == "POST":
        Exspenses.objects.create(
            user = request.user,
            exspense = exspense,
            amount = amount,
        )
def edit_exspense(request, exspense, amount ):
    exspense = get_object_or_404(Exspenses, id = exspense, user = request.user)
    if request.method == "POST":
        exspense.amount = request.POST['amount']
def delete_exspense(request, exspense):
    exspense = get_object_or_404(Exspenses, id = exspense, user = request.user)
    if  request.method == "POST":
        exspense.delete()

# methods for income database modification
def create_income(request, income, amount):
    if request.method == "POST":
        Income.objects.create(
            user = request.user,
            income = income,
            amount = amount,
        )
def edit_income(request, income):
    income = get_object_or_404(Income, id = income, user = request.user)
    if request.method == "POST":
        income.amount = request.POST['amount']
def delete_income(request, income):
    income = get_object_or_404(Income, id = income, user = request.user)
    if request.method == "POST":
        income.delete()
# app/views.py



