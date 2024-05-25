from django.urls import path

from . import views

urlpatterns = [
    path("report-date-range/", views.ReportDateRangeView.as_view(), name="report_date_range"),
    path("report-category/", views.ReportCategoryView.as_view(), name="report_category"),
    path("report-day-graph/", views.ReportDayGraph.as_view(), name="report_day_graph"),
    path("report-week-graph/", views.ReportWeekGraph.as_view(), name="report_week_graph"),
    path("report-month-graph/", views.ReportMonthGraph.as_view(), name="report_month_graph"),
    path(
        "report-most-recent-expenses/",
        views.reportMostRecentView.as_view(),
        name="report_most_recent_expenses",
    ),
    path("report-net/", views.reportNetView.as_view(), name="report_net"),
]
