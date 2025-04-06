from django.shortcuts import render
from django.shortcuts import render
from .models import Transaction, Category
def home(request):
     return render(request,'home.html',{})
def about(request):
     return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
# Create your views here.
# app/views.py


def dashboard(request):
    categories = Category.objects.all()
    transactions = Transaction.objects.all().order_by('-date')

    category_data = []
    for cat in categories:
        spent = sum(t.amount for t in cat.transaction_set.all())
        category_data.append({
            'name': cat.name,
            'budget': cat.budget,
            'spent': spent,
        })

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'category_data': category_data,
    })
