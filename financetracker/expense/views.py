from django.http import Http404
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import csv
from .models import Expense
from .serializers import ExpenseSerializer
from datetime import datetime
current_month = datetime.now().month

class ExpenseListView(APIView):
    """
    API view for retrieving and creating expenses.

    GET request:
    - Retrieves expenses for the authenticated user for the current month.
    - Returns a list of serialized expense objects.

    POST request:
    - Creates a new expense for the authenticated user.
    - Expects the following data in the request body:
        - name: Name of the expense (string)
        - amount: Amount of the expense (float)
        - description: Description of the expense (string)
        - category: ID of the expense category (integer)
    - Returns the serialized expense object of the created expense.

    If any error occurs during retrieval or creation of expenses, appropriate error responses are returned.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            results = (
                Expense.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .order_by("-id")
            )
            serializer = ExpenseSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            data = request.data
            expense = Expense.objects.create(
                name=data["name"],
                amount=data["amount"],
                description=data["description"],
                category_id=data["category"],
                user=request.user,
            )
            serializer = ExpenseSerializer(expense, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to create expense"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        


class ExpenseDetailView(APIView):
    """
    A view for retrieving, updating, and deleting an expense.

    Methods:
    - get_object(pk): Retrieves the expense object with the given primary key.
    - get(request, pk): Retrieves and returns the serialized data of the expense if the user is authorized.
    - put(request, pk): Updates the expense with the provided data if the user is authorized.
    - delete(request, pk): Deletes the expense if the user is authorized.
    - post(request, pk): Creates a duplicate expense if the user is authorized.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        """
        Retrieves the expense object with the given primary key.

        Parameters:
        - pk (int): The primary key of the expense.

        Returns:
        - Expense: The expense object.

        Raises:
        - Http404: If the expense with the given primary key does not exist.
        """
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieves and returns the serialized data of the expense if the user is authorized.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the expense.

        Returns:
        - Response: The serialized data of the expense.

        Raises:
        - Response(status=status.HTTP_401_UNAUTHORIZED): If the user is not authorized to access the expense.
        """
        expense = self.get_object(pk)
        if request.user == expense.user:
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def put(self, request, pk):
        """
        Updates the expense with the provided data if the user is authorized.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the expense.

        Returns:
        - Response: The serialized data of the updated expense.

        Raises:
        - Response(status=status.HTTP_401_UNAUTHORIZED): If the user is not authorized to update the expense.
        """
        expense = self.get_object(pk)
        data = request.data
        if request.user == expense.user:
            expense.name = data["name"]
            expense.amount = data["amount"]
            expense.description = data["description"]
            expense.category_id = data["category"]
            serializer = ExpenseSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, pk):
        """
        Deletes the expense if the user is authorized.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the expense.

        Returns:
        - Response: A response with no content.

        Raises:
        - Response(status=status.HTTP_401_UNAUTHORIZED): If the user is not authorized to delete the expense.
        """
        expense = self.get_object(pk)
        if request.user == expense.user:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def post(self, request, pk):
        """
        Creates a duplicate expense if the user is authorized.

        Parameters:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the expense.

        Returns:
        - Response: The serialized data of the created duplicate expense.

        Raises:
        - Response(status=status.HTTP_401_UNAUTHORIZED): If the user is not authorized to create the duplicate expense.
        """
        expense = self.get_object(pk)
        if request.user == expense.user:
            duplicate_expense = Expense.objects.create(
                name=expense.name,
                amount=expense.amount,
                description=expense.description,
                category_id=expense.category_id,
                user=request.user,
            )
            serializer = ExpenseSerializer(duplicate_expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class ExportExpenseCsv(APIView):
    """
    API view to export expenses as a CSV file.

    This view allows users to download their expenses as a CSV file.
    The CSV file will contain the following columns: name, category, amount, description, budget.
    """

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=expenses.csv"
        writer = csv.writer(response)
        writer.writerow(["name", "category", "amount", "description", "budget"])
        expenses = (
            Expense.objects.filter(user=request.user)
            .filter(date__month=str(current_month))
            .order_by("-id")
        )
        
        for expense in expenses:
            writer.writerow(
                [
                    expense.name,
                    expense.category.name,
                    expense.amount,
                    expense.description,
                    expense.category.budget,
                ]
            )
        return response
