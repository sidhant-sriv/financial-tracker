from category.models import Category
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from income.models import Income
from income.serializers import IncomeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
INCOME = "income"
EXPENSE = "expense"
current_month = datetime.now().month

class ReportDateRangeView(APIView):
    """
    A view for retrieving filtered expense or income data within a specified date range.

    This view requires the user to be authenticated.

    Supported query parameters:
    - from_date: The start date of the date range (format: YYYY-MM-DD).
    - to_date: The end date of the date range (format: YYYY-MM-DD).
    - select: The type of data to retrieve (either 'expense' or 'income').

    Returns a JSON response containing the filtered data and the total sum of expenses or income.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        select = request.GET.get("select")
        try:
            if select == EXPENSE:
                filtered_expense = (
                    Expense.objects.filter(user=request.user)
                    .filter(date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = ExpenseSerializer(filtered_expense, many=True)
                expense_sum = Expense.get_expense_total(
                    from_date, to_date, request.user
                )
                json_data = {"filtered": serializer.data, "total": expense_sum}
                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)

            if select == INCOME:
                filtered_income = (
                    Income.objects.filter(user=request.user)
                    .filter(date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = IncomeSerializer(filtered_income, many=True)
                income_sum = Income.get_income_total(from_date, to_date, request.user)
                json_data = {"filtered": serializer.data, "total": income_sum}

                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Results not found, Invalid parameters"},
                status=status.HTTP_404_NOT_FOUND,
            )


# last 7 days
class ReportDayGraph(APIView):
    """
    API view for generating a graph of daily expenses for the last week.

    Requires authentication.

    Methods:
    - get: Retrieves the daily expenses for the last week and returns a response with the filtered data.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(
                {"filtered": Expense.get_expenses_daily_for_the_week(request.user)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Unable to get daily expenses for the last week"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Report each week of the month
class ReportWeekGraph(APIView):
    """
    API view to retrieve filtered expenses for each week of the month.

    Requires authentication.

    Methods:
    - get: Retrieves filtered expenses for each week of the month for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(
                {"filtered": get_expenses_daily_for_the_week(user=request.user)},
                status=status.HTTP_200_OK,
            )

        except:
            return Response(
                data={"message": "Unable to get expenses for each week of the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Monthly Expenses
class ReportMonthGraph(APIView):
    """
    API view for generating a monthly expense report graph.

    This view requires authentication and returns a filtered dataset of monthly expenses for the year.

    Methods:
    - get: Retrieves the monthly expenses for the year and returns a filtered dataset.

    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = Expense.get_expenses_monthly_for_the_year(request.user)
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get monthly expenses for the year"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReportMostRecentView(APIView):
    """
    API view to retrieve the most recent expenses for the authenticated user.

    Requires authentication.

    Methods:
    - get: Retrieves the most recent expenses for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            filtered = (
                Expense.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .order_by("-id")[:5]
            )
            serializer = ExpenseSerializer(filtered, many=True)
            return Response({"filtered": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get most recent expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReportNetView(APIView):
    """
    API view for retrieving net expenses for the month.

    Requires authentication.

    Methods:
    - get: Retrieves net expenses for the month for the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            category_count = (
                Category.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .all()
                .count()
            )

            data = Expense.get_net_expenses_for_the_month(request.user)
            data[0]["categoryCount"] = category_count

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReportCategoryView(APIView):
    """
    API view for retrieving filtered expense data grouped by categories.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            categories = Category.objects.filter(user=request.user).filter(
                date__month=str(current_month)
            )
            data = []
            for i in categories:
                data.append({"category": i.name, "amount": i.total_expense_cost})
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )

def get_expenses_daily_for_the_week(user):
    filtered = (
        Expense.objects.all()
        .filter(user=user)
        .annotate(week=TruncWeek("date"))
        .values("week")
        .annotate(total=Sum("amount"))
        .order_by("week")
    )
    return filtered

class ReportPortfolioPerformanceSummaryView(APIView):
    """
    A view for retrieving a summary of portfolio performance.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            portfolios = Portfolio.objects.filter(user=request.user)
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get portfolio performance summary"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ReportInvestmentsWeekGraphView(APIView):
    """
    API view for generating a graph of weekly investments for the current month.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=30)
            weekly_investments = (
                Investment.objects.filter(portfolio__user=request.user)
                .filter(date_invested__range=[start_date, end_date])
                .annotate(week=TruncWeek("date_invested"))
                .values("week")
                .annotate(total=Sum("amount"))
                .order_by("week")
            )
            return Response({"filtered": weekly_investments}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get weekly investments for the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )

# Get total investment
class ReportInvestmentsTotalView(APIView):
    """
    API view for generating a graph of total investments for the current month.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=30)
            total_investments = (
                Investment.objects.filter(portfolio__user=request.user)
                .filter(date_invested__range=[start_date, end_date])
                .aggregate(total=Sum("amount"))
            )
            return Response({"filtered": total_investments}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get total investments for the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )