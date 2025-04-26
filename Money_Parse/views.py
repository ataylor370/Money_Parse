import openai
  # Ensure you import openai for API calls
from django.db.models import Sum
from openai import OpenAI
import json
from .models import Transaction, Category, Exspenses, Goal, Income  # Corrected 'Exspenses' to 'Expenses'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import os  # For loading the environment variable
client = OpenAI(api_key= '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')
def get_openai_api_key():
    try:
        # Fetch the API key from the database if it's available
        openai_key = OpenAI.objects.first()  # Assuming the key is stored in the OpenAI model
        if openai_key:
              openai.api_key = openai_key.api_key# Set the API key in the OpenAI client
        else:
            raise ValueError("API key not found in database")
    except Exception as e:
        print(f"Error: {e}")
          # Reset the API key if an error occurs

def get_financial_suggestions(user):
    # Collect relevant user data
    income = Income.objects.filter(user=user).first()
    expenses = Exspenses.objects.filter(user=user).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0  # Fixed typo here
    categories = Category.objects.filter(user=user)
    categories_data = {category.name: category.budget for category in categories}

    # Create a prompt based on user data
    prompt = f"Provide 3 bullet points of financial advice based on the following data:\nIncome: {income}\nExpenses: {expenses}\nCategories: {categories_data}"

    try:
        # Call the OpenAI API with the prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        advice = response.choices[0].message.content.strip()
        return advice
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
def home(request):
     return render(request,'home.html',{})
def about(request):
    request.user = None
    return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # or return str(obj) if you prefer to serialize as a string
    raise TypeError("Type not serializable")


def budget(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    goals = Goal.objects.filter(user=user)
    expenses = Exspenses.objects.filter(user=user)
    # Fix the typo from Exspenses to Expenses

    # Fetch the user's income (assuming each user has one income)
    income = Income.objects.filter(user=user).first()  # Use `.first()` to get the first income object
    total_expense_amount = sum(float(exp.amount) for exp in expenses)  # Ensure correct access to amount

    budget = None
    if income:
        budget = float(income.amount) - total_expense_amount  # Calculate budget if income exists
    # Ensure income exists and is valid
    if income is None or income.amount == 0:
        # If no income or income is 0, handle it as needed (e.g., set to 0 or skip)
        income_amount = 1  # Avoid division by zero, default to 1
    else:
        income_amount = float(income.amount)  # Convert income to float

    total_category_amount = sum(float(category.budget) for category in categories)

    remain = income_amount  - total_expense_amount
    # Calculate the remaining budget
    remaining = budget - total_category_amount if budget is not None else 0

    # Formatting the data for Google Charts API
    chart_data = [['Category', 'Amount']]

    for expense in expenses:
        expense_percentage = (float(expense.amount) / income_amount) * 100 if income_amount != 0 else 0  # Ensure division by float
        chart_data.append([expense.expense, expense.amount])

    # Serialize chart_data with custom decimal serializer
    chart_data_json = json.dumps(chart_data, default=decimal_default)

    return render(request, 'Budget.html', {
        'categories': categories,
        'goals': goals,
        'chart_data': chart_data_json,
        'income': income,
        'budget': budget,
        'remaining': remaining,
        'remain': remain,
        'expenses': expenses,
        'total_expense_amount': total_expense_amount,
    })


def dashboard(request):
    user = request.user
    categories = Category.objects.filter(user = user)
    transactions = Transaction.objects.filter(user=user).order_by('-date', '-id')
    financial_advice = get_financial_suggestions(request.user)
    financial_advice_list = financial_advice.split('\n') if financial_advice else []

    category_data = []
    for cat in categories:
        percent = float((cat.spent / cat.budget) * 100) if cat.budget > 0 else 0
        category_data.append({
            'name': cat.name,
            'budget': cat.budget,
            'spent': cat.spent,
            'percent': percent,
        })

    return render(request, 'dashboard.html', {
        'categories': categories,
        'transactions': transactions,
        'category_data': category_data,
        'financial_advice': financial_advice_list,
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
            user=request.user,
            name=request.POST.get('new_category'),
            budget=request.POST.get('new_budget'),
        )
        return redirect('budget')

def edit_category(request):
    if request.method == "POST":
        current_name = request.POST.get('category')
        new_name = request.POST.get('new_category')
        new_budget = request.POST.get('new_budget')
        category = get_object_or_404(Category, name = current_name, user=request.user)
        category.name = new_name
        category.budget = new_budget
        category.save()
        return redirect('budget')
def delete_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        category = get_object_or_404(Category, name=category_name, user=request.user)
        category.delete()
        return redirect('budget')

# methods for Goal database modification
def create_goal(request):
    if request.method == "POST":
        new_goal = request.POST.get('new_goal')
        Goal.objects.create(
            user = request.user,
            goal = new_goal,
        )
        return redirect('budget')
def edit_goal(request):
    if request.method == "POST":
        goal_number = request.POST.get('goal_number')
        goal = get_object_or_404(Goal, number=goal_number, user=request.user)
        goal.goal = request.POST.get('new_goal')
        goal.save()
        return redirect('budget')
def delete_goal(request):
    if request.method == "POST":
        goal_number = request.POST.get('goal_number')
        goal = get_object_or_404(Goal, number=goal_number, user=request.user)
        goal.delete()
    # renumbering goals after deletion made
    remaining_goals = Goal.objects.filter(user=request.user).order_by('number')
    for idx, goal in enumerate(remaining_goals, start=1):
        goal.number = idx
        goal.save()
    return redirect('budget')


# methods for exspense database modification
def create_expense(request):
    if request.method == "POST":
        name = request.POST.get("new_expense")
        amount = request.POST.get("new_amount")
        Exspenses.objects.create(expense=name, amount=amount, user=request.user)
        return redirect("budget")
def edit_expense(request):
    if request.method == "POST":
        expense_name = request.POST.get('expense')
        expense = get_object_or_404(Exspenses, id=expense_name, user=request.user)
        expense.expense = request.POST.get('new_expense')
        expense.amount = request.POST.get('new_amount')
        expense.save()
        return redirect('budget')
def delete_expense(request):
    if  request.method == "POST":
        expense_name = request.POST.get('expense')
        expense = get_object_or_404(Exspenses, expense =expense_name, user=request.user)
        expense.delete()
        return redirect('budget')

# methods for income database modification
def edit_income(request):
    if request.method == "POST":
        income = get_object_or_404(Income, user=request.user)
        income.amount = request.POST.get('amount')
        income.save()
        return redirect('budget')

@login_required
def transaction_list(request):
    # pull this user’s transactions, newest first
    txns = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction_list.html', {
        'transactions': txns,
    })
# app/views.py



