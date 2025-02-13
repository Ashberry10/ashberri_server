from account.modelapiview import AllUser, FriendStatusAndrankById
from account.views import GetAllUser, UpdateUser,UserProfileView , UserDeleteView, UserLoginView,UserRegistrationView
from django.urls import path,include



urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('users/', GetAllUser.as_view(),name='getallusers'), NOTE --this api can be use later on, instead of this api use http://127.0.0.1:8000/account/friendStatusAndrank/
    # path('users/<int:id>',GetAllUser.as_view(), ),NOTE --this api can be use later on instead of this api use http://127.0.0.1:8000/account/friendStatusAndrankById/?id=1
    # path('search/', include('customsearch.urls')),
    path('friendStatusAndrank/', AllUser.as_view(), name='friend_status_and_rank'),
    path('friendStatusAndrankById/', FriendStatusAndrankById.as_view(), name='friendStatusAndrankById'),
    path('deleteuser/<int:id>', UserDeleteView.as_view(), name='user-delete'),
] 

