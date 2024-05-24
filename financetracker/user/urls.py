from django.urls import path
from .views import CustomAuthToken, RegisterUser, UserProfile, UsersList, UsersDetail

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('user/register/', RegisterUser.as_view(), name='register_user'),
    path('user/profile/', UserProfile.as_view(), name='user_profile'),
    path('users/', UsersList.as_view(), name='users_list'),
    path('users/<int:pk>/', UsersDetail.as_view(), name='users_detail'),
]
