from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from income.serializers import IncomeSerializer
from datetime import datetime, time, timedelta

from .models import Income

current_month = datetime.now().date().month

class IncomeListView(APIView):
    """
    API view for managing income records.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Retrieve income records for the authenticated user.

        Returns:
            A Response object containing the serialized income records.
        """
        try:
            results = (
                Income.objects.all()
                .filter(user=request.user)
                .filter(date__month=str(current_month))
            )
            serializer = IncomeSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve income"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        """
        Create a new income record for the authenticated user.

        Args:
            request: The HTTP request object containing the income data.

        Returns:
            A Response object containing the serialized newly created income record.
        """
        try:
            data = request.data
            income = Income.objects.create(
                name=data["name"],
                amount=data["amount"],
                description=data["description"],
                user=request.user,
            )
            serializer = IncomeSerializer(income, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to add new income"}, status=status.HTTP_400_BAD_REQUEST
            )


from django.http import Http404
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from income.models import Income
from income.serializers import IncomeSerializer

class IncomeDetailView(APIView):
    """
    A view for retrieving, updating, deleting, and duplicating an income object.

    Methods:
    - get_object(pk): Retrieves the income object with the specified primary key.
    - get(request, pk): Retrieves the income object and returns its serialized data.
    - put(request, pk): Updates the income object with the provided data.
    - delete(request, pk): Deletes the income object.
    - post(request, pk): Duplicates the income object with the current date.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        """
        Retrieves the income object with the specified primary key.

        Parameters:
        - pk (int): The primary key of the income object.

        Returns:
        - Income: The income object with the specified primary key.

        Raises:
        - Http404: If the income object with the specified primary key does not exist.
        """
        try:
            return Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieves the income object and returns its serialized data.

        Parameters:
        - request (Request): The HTTP request object.
        - pk (int): The primary key of the income object.

        Returns:
        - Response: The serialized data of the income object.

        Raises:
        - Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN):
          If the user is not permitted to access the income object.
        """
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """
        Updates the income object with the provided data.

        Parameters:
        - request (Request): The HTTP request object.
        - pk (int): The primary key of the income object.

        Returns:
        - Response: The serialized data of the updated income object.

        Raises:
        - Http404: If the income object with the specified primary key does not exist.
        """
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        """
        Deletes the income object.

        Parameters:
        - request (Request): The HTTP request object.
        - pk (int): The primary key of the income object.

        Returns:
        - Response: A response with no content.

        Raises:
        - Http404: If the income object with the specified primary key does not exist.
        """
        income = self.get_object(pk)
        if request.user == income.user:
            income.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        """
        Duplicates the income object with the current date.

        Parameters:
        - request (Request): The HTTP request object.
        - pk (int): The primary key of the income object to be duplicated.

        Returns:
        - Response: The serialized data of the new income object.

        Raises:
        - Http404: If the income object with the specified primary key does not exist.
        """
        income = self.get_object(pk)
        if request.user == income.user:
            new_income = Income(
                user=income.user,
                name=income.name,
                amount=income.amount,
                date=datetime.now(), 
                description=income.description
            )
            new_income.save()
            serializer = IncomeSerializer(new_income)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)
