# Import necessary modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, UserSerializerWithToken
from django.http import Http404
import logging

# Configure logging
logger = logging.getLogger(__name__)

class RegisterUser(APIView):
    """
    View for registering a new user.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Create a new user.
        """
        logger.debug(f'Request data: {request.data}')
        data = request.data
        try:
            # Validate and handle password separately
            password = data.pop('password')
            user = User.objects.create(**data)
            user.set_password(password)
            user.save()
            # Generate token
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializerWithToken(user, many=False)
            return Response({'token': token.key, **serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Error creating user: {e}')
            return Response({'error': 'User not created, please recheck input parameters'}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication token view.
    """
    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return token.
        """
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """
    View for retrieving user profile.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Retrieve user profile.
        """
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersList(APIView):
    """
    View for retrieving list of users.
    """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Retrieve list of users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersDetail(APIView):
    """
    View for retrieving, updating, or deleting a specific user.
    """
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self, pk):
        """
        Get user object by primary key.
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieve a specific user.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Update a specific user.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete a specific user.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
