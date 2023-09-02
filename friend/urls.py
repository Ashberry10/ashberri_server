from django.urls import path
# from account.modelapiview import ModelapiView
from  account import views
from django.urls import path,include



from friend.views import ViewAllFriendRequestAPIView,AcceptOrRejectFriendRequestAPIView,UnfriendAPIView,CancelFriendRequestAPIView,FriendRequestAPIView,GetAllUserFriendStatusAPIView


urlpatterns = [
	# path('list/<user_id>', friends_list_view, name='list'),
	# path('friend_remove/', remove_friend, name='remove-friend'),
    # path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    # path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),
    path('friend-requests/',ViewAllFriendRequestAPIView.as_view(), name='friend_requests'),
    path('accept_or_reject_friendrequest/', AcceptOrRejectFriendRequestAPIView.as_view(), name='accept_friend_request'),
    path('unfriend/', UnfriendAPIView.as_view(), name='unfriend'),
    path('cancel-friend-request/', CancelFriendRequestAPIView.as_view(), name='cancel-friend-request'),
    path('friend-request/', FriendRequestAPIView.as_view(), name='friend-request'),
    # path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    # path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
 ]