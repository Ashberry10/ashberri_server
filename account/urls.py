from account.modelapiview import AllUser, FriendStatusAndCompatibilityById
from account.views import GetAllUser, UpdateUser, UserDeleteView, UserLoginView, UserProfileView,UserRegistrationView
from django.urls import path



urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', GetAllUser.as_view(),name='getallusers'),
    path('users/<int:id>',GetAllUser.as_view(), ),

    path('friendStatusAndCompatibility/', AllUser.as_view(), name='friend_status_and_compatibility'),
    path('friendStatusAndCompatibilityById/', FriendStatusAndCompatibilityById.as_view(), name='friendStatusAndCompatibilitById'),
    path('deleteuser/<int:id>', UserDeleteView.as_view(), name='user-delete'),
] 

