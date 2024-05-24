from django.urls import path

from . import views

app_name = "category"

urlpatterns = [
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
