from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, InvestmentListView, InvestmentDetailView

urlpatterns = [
    path('portfolios/', PortfolioListView.as_view(), name='portfolio-list'),
    path('portfolios/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('portfolios/<int:portfolio_pk>/investments/', InvestmentListView.as_view(), name='investment-list'),
    path('investments/<int:pk>/', InvestmentDetailView.as_view(), name='investment-detail'),
]
