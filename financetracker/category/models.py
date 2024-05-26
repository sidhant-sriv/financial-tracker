from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from expense.models import Expense
from django.db.models.signals import post_save

class Category(models.Model):
    user = models.ForeignKey(User, related_name="categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.name

    @property
    def total_expense_cost(self):
        expenses = Expense.objects.filter(category=self.id)
        return sum(expense.amount for expense in expenses)

    @property
    def remaining_budget(self):
        if self.budget is not None:
            return self.budget - self.total_expense_cost
        return None

    @property
    def is_budget_exceeded(self):
        if self.budget is not None:
            return self.total_expense_cost > self.budget
        return False

# Create default categories with budgets when a new user is created
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(user=instance, name="Food and Drinks")
        Category.objects.create(user=instance, name="Transport")
        Category.objects.create(user=instance, name="Groceries")
        Category.objects.create(user=instance, name="Personal")
        Category.objects.create(user=instance, name="Services")
        Category.objects.create(user=instance, name="Miscellaneous")
