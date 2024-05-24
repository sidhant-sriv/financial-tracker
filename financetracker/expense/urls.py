from django.urls import path

from . import views

urlpatterns = [
    path("expense/", views.ExpenseListView.as_view(), name="expense_list"),
    path("expense/<int:pk>/", views.ExpenseDetailView.as_view(), name="expense_detail"),
    path("expense/export-csv/", views.ExportExpenseCsv.as_view(), name="export_csv"),

]
