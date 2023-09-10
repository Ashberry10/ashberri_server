from django.urls import path
from  account import views
from django.urls import path,include

from friend.views import FriendAPIView, ViewAllFriendRequestAPIView,AcceptOrRejectFriendRequestAPIView,UnfriendAPIView,CancelFriendRequestAPIView,FriendRequestAPIView


urlpatterns = [
    path('',FriendAPIView.as_view(),name='friend_list'),
    path('friend-requests/',ViewAllFriendRequestAPIView.as_view(), name='friend_requests'),
    path('accept_or_reject_friendrequest/', AcceptOrRejectFriendRequestAPIView.as_view(), name='accept_friend_request'),
    path('unfriend/', UnfriendAPIView.as_view(), name='unfriend'),
    path('cancel-friend-request/', CancelFriendRequestAPIView.as_view(), name='cancel-friend-request'),
    path('friend-request/', FriendRequestAPIView.as_view(), name='friend-request'),
]