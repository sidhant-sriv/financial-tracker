#urls for income 
from django.urls import path, include
from . import views

urlpatterns = [
    path("income/", views.IncomeListView.as_view(), name="income_list"),
    path("income/<int:pk>/", views.IncomeDetailView.as_view(), name="income_detail"),
]
