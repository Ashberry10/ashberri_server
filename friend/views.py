from django.shortcuts import render
import json
# Create your views here.
from account.models import UserManager,User
from friend.models import  FriendShip

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import FriendShipSerializer,FriendRequestSerializer


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendShipSerializer(data=request.data)
        if serializer.is_valid():
            receiver = serializer.validated_data.get('receiver')
            receiver_name = receiver.name  # Assuming `name` is a field in the receiver model
            # receiver_name = serializer.validated_data.get('receiver').name

            # Set the sender as the logged-in user
            friend_request = serializer.save(sender=request.user, receiver=receiver)
            return Response({
                'status': 'success',
                'message': f"Friend request has been sent successfully to {receiver_name}",
                'friend_request_id': friend_request.id,
                'receiver': receiver.id
            }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response({'status': 'error', 'message': 'Failed to send friend request', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

class CancelFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = FriendShipSerializer(data=request.data)
        
        if serializer.is_valid():
            receiver = serializer.validated_data.get('receiver')

            friend_request = FriendShip.objects.filter(receiver=receiver.id, sender=request.user).first()

            if friend_request:
                friend_request.delete()
                return Response({'message': 'Friend request canceled successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AcceptOrRejectFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendShipSerializer(data=request.data)
        
        if serializer.is_valid():
            receiver = serializer.validated_data.get('receiver')
            
            try:
                friend_request = FriendShip.objects.get(receiver=receiver, sender=request.user)
            except FriendShip.DoesNotExist:
                return Response({'message': 'Friend request does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Perform any additional checks or validations here
            
            # action = serializer.validated_data.get('action')
            action = request.data.get('action')
            
            if action == 'accept':
                friend_request.accept()
                return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.reject()
                return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewAllFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        friend_requests = FriendShip.objects.filter(receiver_id=user_id)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        serialized_data = serializer.data

        # Update serialized data to include sender's name
        for data in serialized_data:
            sender_id = data['sender']
            sender_name = User.objects.get(id=sender_id).name
            data['sender_name'] = sender_name

        friend_request_count = len(serialized_data)

        if friend_request_count == 0:
            return Response({'message': 'No friend requests found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'message': 'All friend requests',
            'total_friend_requests': friend_request_count,
            'friend_requests': serialized_data
        }, status=status.HTTP_200_OK)



class UnfriendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver = request.data.get('receiver')
        
        try:
            friendShip = FriendShip.objects.filter(sender=request.user, receiver=receiver).first() \
                         or FriendShip.objects.filter(receiver=request.user, sender=receiver).first()
        except FriendShip.DoesNotExist:
            return Response({'message': 'Friendship does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        friendShip.delete()
        
        return Response({'message': 'Unfriended successfully.'}, status=status.HTTP_200_OK)

