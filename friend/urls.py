from django.urls import path
from account.views import UserLoginView,UserRegistrationView,AllUser,UserProfileView,UpdateUser,UserDeleteView
from account.modelapiview import ModelapiView
from  account import views
from django.urls import path,include



from friend.views import SendFriendRequestView 


urlpatterns = [
	# path('list/<user_id>', friends_list_view, name='list'),
	# path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request/', SendFriendRequestView.as_view(), name='friend_request'),
    # path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),
    # path('friend_requests/<user_id>/', friend_requests, name='friend-requests'),
    # path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    # path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
 ]