from django.contrib.auth.models import User
from django.db import models
import calendar
from income.models import Income
from datetime import timedelta, datetime

today = datetime.now().date()
one_week_ago = today - timedelta(days=7)
current_month = today.month

class Expense(models.Model):
    user = models.ForeignKey(
        User, related_name="expenses", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    amount = models.FloatField(default=0, blank=True)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_expense_total(from_date, to_date, user):
        if from_date == to_date:
            filtered_expense = Expense.objects.filter(user=user).filter(date=to_date)
            expense_sum = round(
                (sum(expense.amount for expense in filtered_expense)), 2
            )
            return expense_sum
        else:
            filtered_expense = (
                Expense.objects.filter(user=user)
                .filter(date__range=(from_date, to_date))
                .order_by("-id")
            )
            expense_sum = round(
                (sum(expense.amount for expense in filtered_expense)), 2
            )
            return expense_sum

    @staticmethod
    def get_expenses_daily_for_the_week(user):
        data = []
        delta = today - one_week_ago
        for i in range(delta.days + 1):
            day = one_week_ago + timedelta(days=i)
            queryset = Expense.objects.filter(user=user).filter(date__startswith=day)
            day_cost = sum([expense.amount for expense in queryset])
            data.append({"day": day, "amount": day_cost})
        return data

    @staticmethod
    def get_expenses_monthly_for_the_year(user):
        data = []
        for i in range(1, 13):
            months = Expense.objects.filter(user=user).filter(date__month=i)
            month_cost = sum([expense.amount for expense in months])
            month_name = calendar.month_name[i]
            data.append({"month": month_name, "amount": month_cost})
        return data

    @staticmethod
    def get_net_expenses_for_the_month(user):
        total_expenses = Expense.objects.filter(user=user).filter(
            date__month=str(current_month)
        )
        expense_count = (
            Expense.objects.filter(user=user)
            .filter(date__month=str(current_month))
            .all()
            .count()
        )
        expense_sum = round((sum(expense.amount for expense in total_expenses)), 2)
        total_income = Income.objects.filter(user=user).filter(
            date__month=str(current_month)
        )
        income_count = (
            Income.objects.filter(user=user)
            .filter(date__month=str(current_month))
            .all()
            .count()
        )
        income_sum = round((sum(income.amount for income in total_income)), 2)
        net_value = round((income_sum - expense_sum), 2)
        data = (
            {
                "expense": expense_sum,
                "income": income_sum,
                "net": net_value,
                "incomeCount": income_count,
                "expenseCount": expense_count,
            },
        )

        return data
