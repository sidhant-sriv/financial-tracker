from django.urls import path
from . import views

urlpatterns = [
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
