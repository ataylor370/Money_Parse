from .models import Category, Transaction, Incomes, Exspenses, Goal
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # Customize fields shown

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'user')
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date', 'category', 'user')
@admin.register(Incomes)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('income', 'amount', 'user')
@admin.register(Exspenses)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense', 'amount', 'user')
@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('goal','number', 'user')
# Register your models here.