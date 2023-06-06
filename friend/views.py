from django.shortcuts import render
import json
# Create your views here.
from account.models import UserManager,User
from friend.models import FriendRequest

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import User

from rest_framework.views import APIView

from .serializers import FriendRequestSerializer

# def send_friend_request(request, *args, **kwargs):
#     user = request.user
#     payload = {}
# 	if request.method == "POST" and user.is_authenticated:
# 		user_id = request.POST.get("receiver_user_id")
# 		if user_id:
# 			receiver = Account.objects.get(pk=user_id)
# 			try:
# 				# Get any friend requests (active and not-active)
# 				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
# 				# find if any of them are active (pending)
# 				try:
# 					for request in friend_requests:
# 						if request.is_active:
# 							raise Exception("You already sent them a friend request.")
# 					# If none are active create a new friend request
# 					friend_request = FriendRequest(sender=user, receiver=receiver)
# 					friend_request.save()
# 					payload['response'] = "Friend request sent."
# 				except Exception as e:
# 					payload['response'] = str(e)
# 			except FriendRequest.DoesNotExist:
# 				# There are no friend requests so create one.
# 				friend_request = FriendRequest(sender=user, receiver=receiver)
# 				friend_request.save()
# 				payload['response'] = "Friend request sent."

# 			if payload['response'] == None:
# 				payload['response'] = "Something went wrong."
# 		else:
# 			payload['response'] = "Unable to sent a friend request."
# 	else:
# 		payload['response'] = "You must be authenticated to send a friend request."
# 	return HttpResponse(json.dumps(payload), content_type="application/json")



class SendFriendRequestView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"response": "You must be authenticated to send a friend request."},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = request.data.get("receiver_user_id")
        if not user_id:
            return Response({"response": "Unable to send a friend request."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        receiver = get_object_or_404(User, pk=user_id)
        
        friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
        for friend_request in friend_requests:
            if friend_request.is_active:
                return Response({"response": "You already sent them a friend request."},
                                status=status.HTTP_400_BAD_REQUEST)
    
        friend_request = FriendRequest(sender=user, receiver=receiver)
        friend_request.save()
        
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)