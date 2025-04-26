from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from Money_Parse.models import Exspenses,Category,Goal,Income
from .forms import CustomUserCreationForm
from django.contrib import messages


def signup_view(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Initialize session variables
            request.session['expenses'] = []
            request.session['goals'] = []
            request.session['categories'] = []

            return redirect('accounts.account_initialization')

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

def account_initialization_view(request):
    if 'expenses' not in request.session:
        request.session['expenses'] = []
    if 'goals' not in request.session:
        request.session['goals'] = []
    if 'categories' not in request.session:
        request.session['categories'] = []

    income = getattr(request.user, 'income', None)
    expenses = request.session.get('expenses', [])
    goals = request.session.get('goals', [])
    categories = request.session.get('categories', [])

    total_expense_amount = sum(float(exp['amount']) for exp in expenses)

    if income is None or income.amount == 0:
        income_amount = 1  # Avoid division by zero
    else:
        income_amount = float(income.amount)

    # Calculate budget and remain
    budget = income_amount - total_expense_amount
    remain = income_amount - total_expense_amount

    total_category_amount = sum(float(category['amount']) for category in categories)
    remaining = budget - total_category_amount if budget is not None else 0

    if request.method == 'POST' and 'submit' in request.POST:
        user = request.user
        for expense_data in expenses:
            Exspenses.objects.create(
                user=user,
                expense=expense_data['expense'],
                amount=expense_data['amount']
            )
        for goal_data in goals:
            Goal.objects.create(
                user=user,
                goal=goal_data['goal'],
            )
        for category_data in categories:
            Category.objects.create(
                user=user,
                name=category_data['category'],
                budget=category_data['amount'],
            )

        # Clear session after saving
        request.session['expenses'] = []
        request.session['goals'] = []
        request.session['categories'] = []

        return redirect('dashboard')

    return render(request, 'accounts/account_initialization.html', {
        'expenses': expenses,
        'goals': goals,
        'categories': categories,
        'income': income,
        'budget': budget,
        'remaining': remaining,
        'remain': remain,
    })


def login_view(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
def logout_view(request):
        logout(request)
        return redirect('about')



@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('about')

def add_income_view(request):
    if request.method == 'POST':
        if hasattr(request.user, 'income'):
            # user already has income
            messages.error(request, 'You have already set your income.')
        else:
            amount = request.POST.get('amount')
            Income.objects.create(user=request.user, amount=amount)
            messages.success(request, 'Income added successfully!')
    return redirect('accounts.account_initialization')
def add_expense_view(request):
    if request.method == 'POST':
        expense_name = request.POST.get('expense')
        amount = request.POST.get('amount')

        # Store the expense in session temporarily
        expenses = request.session.get('expenses', [])
        expenses.append({'expense': expense_name, 'amount': amount})
        request.session['expenses'] = expenses
        request.session.modified = True  # Ensure the session is updated

    return redirect('accounts.account_initialization')

def add_category_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')

        # Store the category in session temporarily
        categories = request.session.get('categories', [])
        categories.append({'category': category, 'amount': amount})
        request.session['categories'] = categories
        request.session.modified = True  # Ensure the session is updated

    return redirect('accounts.account_initialization')

def add_goal_view(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')

        # Store the goal in session temporarily
        goals = request.session.get('goals', [])
        goals.append({'goal': goal})
        request.session['goals'] = goals
        request.session.modified = True  # Ensure the session is updated

    return redirect('accounts.account_initialization')
