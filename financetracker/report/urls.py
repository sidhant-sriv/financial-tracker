from django.urls import path

from . import views

urlpatterns = [
    path("report-date-range/", views.ReportDateRangeView.as_view(), name="report_date_range"),
    path("report-category/", views.ReportCategoryView.as_view(), name="report_category"),
    path("report-day-graph/", views.ReportDayGraph.as_view(), name="report_day_graph"),
    path("report-week-graph/", views.ReportWeekGraph.as_view(), name="report_week_graph"),
    path("report-month-graph/", views.ReportMonthGraph.as_view(), name="report_month_graph"),
    path("report-most-recent-expenses/",views.ReportMostRecentView.as_view(),name="report_most_recent_expenses"),
    path("report-net/", views.ReportNetView.as_view(), name="report_net"),
    path("report-portfolios/", views.ReportPortfolioPerformanceSummaryView.as_view(), name="report_portfolios"),
    path("report-weekly-investments/", views.ReportInvestmentsWeekGraphView.as_view(), name="report_weekly_investments"),
    path("report-total-investments/", views.ReportInvestmentsTotalView.as_view(), name="report_total_investments"),

]
