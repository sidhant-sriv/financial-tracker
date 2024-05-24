from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    """
    API view for listing and creating categories.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Get method to retrieve categories for the authenticated user.

        Returns:
            A Response object with the serialized category data and a status code.
        """
        try:
            category = Category.objects.filter(user=request.user)
            serializer = CategorySerializer(category, many=True)
            data = {"filtered": serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Unable to get categories"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """
        Post method to create a new category for the authenticated user.

        Returns:
            A Response object with the serialized category data and a status code.
        """
        try:
            data = request.data
            category = Category.objects.create(name=data["name"], user=request.user)
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to create category"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


class CategoryDetailView(APIView):
    """
    A view for retrieving, updating, and deleting a specific category.

    Methods:
    - get_object(pk): Retrieves a category object based on the provided primary key.
    - get(request, pk): Retrieves the details of a category.
    - put(request, pk): Updates the details of a category.
    - delete(request, pk): Deletes a category.

    Attributes:
    - permission_classes: A tuple containing the permission classes required for accessing this view.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        """
        Retrieves a category object based on the provided primary key.

        Parameters:
        - pk: The primary key of the category.

        Returns:
        - The category object.

        Raises:
        - Http404: If the category with the provided primary key does not exist.
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieves the details of a category.

        Parameters:
        - request: The request object.
        - pk: The primary key of the category.

        Returns:
        - If the user is authorized to access the category, returns the serialized category data with a status code of 200.
        - If the user is not authorized to access the category, returns a "Forbidden, Not Authorized" message with a status code of 403.
        - If there is an error while retrieving the category details, returns an "Unable to get category detail" message with a status code of 400.
        """
        category = self.get_object(pk)
        if request.user == category.user:
            try:
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Unable to get category detail"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def put(self, request, pk):
        """
        Updates the details of a category.

        Parameters:
        - request: The request object.
        - pk: The primary key of the category.

        Returns:
        - If the user is authorized to update the category and the provided parameters are valid, returns the serialized updated category data with a status code of 200.
        - If the user is not authorized to update the category, returns a "Forbidden, Not Authorized" message with a status code of 403.
        - If the provided parameters are invalid, returns an "Invalid parameters" message with a status code of 400.
        - If there is an error while updating the category, returns an "Unable to update category" message with a status code of 400.
        """
        category = self.get_object(pk)
        if request.user == category.user:
            try:
                serializer = CategorySerializer(category, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        data={"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except:
                return Response(
                    data={"message": "Unable to update category"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, pk):
        """
        Deletes a category.

        Parameters:
        - request: The request object.
        - pk: The primary key of the category.

        Returns:
        - If the user is authorized to delete the category, returns a status code of 204 (No Content).
        - If the user is not authorized to delete the category, returns a "Forbidden, Not Authorized" message with a status code of 403.
        """
        category = self.get_object(pk)
        if request.user == category.user:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"message": "Forbidden, Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )