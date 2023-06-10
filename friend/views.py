from django.shortcuts import render
import json
# Create your views here.
from account.models import UserManager,User
from friend.models import FriendRequest

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.permissions import IsAuthenticated
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




# def friend_requests(request, *args, **kwargs):
#     	context = {}
# 	user = request.user
# 	if user.is_authenticated:
# 		user_id = kwargs.get("user_id")
# 		account = Account.objects.get(pk=user_id)
# 		if account == user:
# 			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
# 			context['friend_requests'] = friend_requests
# 		else:
# 			return HttpResponse("You can't view another users friend requets.")
# 	else:
# 		redirect("login")
# 	return render(request, "friend/friend_requests.html", context)


# class FriendRequestAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         user = request.user
#         if user.is_authenticated:
#             account = get_object_or_404(User, pk=id)
#             if account == user:
#                 friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
#                 serializer = FriendRequestSerializer(friend_requests, many=True)
#                 return Response(serializer.data)
#             else:
#                 return Response("You can't view another user's friend requests.")
#         else:
#             return Response(status=401)







# class SendFriendRequestView(APIView):  
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         if not user.is_authenticated:
#             return Response({"response": "You must be authenticated to send a friend request."},
#                             status=status.HTTP_401_UNAUTHORIZED)
        
#         user_id = request.data.get("receiver_user_id")
#         if not user_id:
#             return Response({"response": "Unable to send a friend request."},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         receiver = get_object_or_404(User, pk=user_id)
        
#         friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
#         for friend_request in friend_requests:
#             if friend_request.is_active:
#                 return Response({"response": "You already sent them a friend request."},
#                                 status=status.HTTP_400_BAD_REQUEST)
    
#         friend_request = FriendRequest(sender=user, receiver=receiver)
#         friend_request.save()
        
#         serializer = FriendRequestSerializer(friend_request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SendFriendRequestView(APIView):
#     # authentication_classes = [YourAuthenticationClass]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = FriendRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             receiver_user_id = serializer.validated_data['receiver_user_id']
#             try:
#                 receiver = User.objects.get(pk=receiver_user_id)
#                 friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
#                 for friend_request in friend_requests:
#                     if friend_request.is_active:
#                         return Response({"response": "You already sent them a friend request."}, status=status.HTTP_400_BAD_REQUEST)
#                 friend_request = FriendRequest(sender=user, receiver=receiver)
#                 friend_request.save()
#                 return Response({"response": "Friend request sent."}, status=status.HTTP_201_CREATED)
#             except User.DoesNotExist:
#                 return Response({"response": "Invalid receiver_user_id."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class SendFriendRequestView(APIView):
#     # authentication_classes = [YourAuthenticationClass]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = FriendRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             # receiver_user_id = serializer.validated_data['receiver_user_id']
#             # receiver_user_id = 6
#             # receiver_user_id = serializer.validated_data.get('receiver_user_id')
#             receiver_user_id = serializer.validated_data.get('receiver_user_id')
#             if receiver_user_id is None:
#                 return Response({"response": "receiver_user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
#             try:
#                 receiver = User.objects.get(pk=receiver_user_id)
#                 friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
#                 for friend_request in friend_requests:
#                     if friend_request.is_active:
#                         return Response({"response": "You already sent them a friend request."}, status=status.HTTP_400_BAD_REQUEST)
#                 friend_request = FriendRequest(sender=user, receiver=receiver)
#                 friend_request.save()
#                 return Response({"response": "Friend request sent."}, status=status.HTTP_201_CREATED)
#             except User.DoesNotExist:
#                 return Response({"response": "Invalid receiver_user_id."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendFriendRequestView(APIView):
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        friend_requests = FriendRequest.objects.filter(receiver_id=user_id)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)