from django.db import models
from django.contrib.auth.models import User
import datetime

class Portfolio(models.Model):
    user = models.ForeignKey(User, related_name="portfolios", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    budget = models.FloatField(default=0)  # New field for budget
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        return sum(investment.value for investment in self.investments.all())

    @property
    def total_invested(self):
        return sum(investment.amount for investment in self.investments.all())

    @property
    def total_return(self):
        return self.total_value - self.total_invested

    @property
    def remaining_budget(self):
        return self.budget - self.total_invested


class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name="investments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    value = models.FloatField()
    description = models.TextField(blank=True, null=True)
    date_invested = models.DateField(auto_now_add=True)  # Date when the investment was made
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def return_on_investment(self):
        return self.value - self.amount
