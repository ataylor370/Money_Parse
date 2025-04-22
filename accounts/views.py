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
        return redirect('dashboard')

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

    expenses = request.session.get('expenses', [])
    goals = request.session.get('goals', [])
    categories = request.session.get('categories', [])

    if request.method == 'POST' and 'submit' in request.POST:
        user = request.user
        # Ensure data exists before processing
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
            # Clear session after saving data
        request.session['expenses'] = []
        request.session['goals'] = []
        request.session['categories'] = []

            # Redirect after successful initialization
        return redirect('dashboard')  # Or wherever you'd like to redirect

    return render(request, 'accounts/account_initialization.html', {
        'expenses': expenses,
        'goals': goals,
        'categories': categories
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

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
    if request.method == 'POST':
        logout(request)
        return redirect('accounts.login')



@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('accounts.signup')
    return render(request, 'accounts/delete_confirm.html')

def add_income_view(request):
    if request.method == 'POST':
        if hasattr(request.user, 'income'):
            # user already has income
            messages.error(request, 'You have already set your income.')
        else:
            source = request.POST.get('source')
            amount = request.POST.get('amount')
            Income.objects.create(user=request.user, source=source, amount=amount)
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
