from django.shortcuts import render
import json
from account.models import UserManager,User
from friend.models import  FriendShip
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from account.serializers import UserProfileSerializer
from .serializers import FriendShipSerializer,FriendRequestSerializer,FriendShipStatusSerializer,AcceptOrRejectFriendRequestSerializer


import joblib
model = joblib.load('./ABmodel.joblib')

class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendShipSerializer(data=request.data)
        if serializer.is_valid():
            receiver = serializer.validated_data.get('receiver')
            receiver_name = receiver.name  # Assuming `name` is a field in the receiver model
            logged_in_user = request.user

            # Check if a friend request already exists
            friend_request = FriendShip.objects.filter(receiver=receiver, sender=logged_in_user).first()

            if friend_request:
                return Response({'status': 'error', 'message': 'Friend request already sent.'}, status=status.HTTP_409_CONFLICT)
            #campatability start
            logged_in_serializer = UserProfileSerializer(logged_in_user)
            logged_in_user_name = logged_in_serializer.data['name']
            c_first = logged_in_serializer.data['C_second']
            d_first = logged_in_serializer.data['D_second']
            logged_in_user_id = logged_in_serializer.data['id']

            friend = User.objects.get(id=receiver.id)
            friend_serializer = UserProfileSerializer(friend)
            friend_name = friend_serializer.data['name']

            result = model.predict([[d_first, c_first, friend_serializer.data['C_second'], friend_serializer.data['D_second']]])
            #compatibility end
            serializer.validated_data['compatibility'] = result


            # Set the sender as the logged-in user and create the friend request
            friend_request = serializer.save(sender=logged_in_user)


            return Response({
                'status': 'success',
                'message': f"Friend request has been sent successfully to {receiver_name}",
                'friend_request_id': friend_request.id,
                'receiver': receiver.id,
                'compatability': serializer.data['compatibility']
            }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response({'status': 'error', 'message': 'Failed to send friend request', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = FriendShipSerializer(data=request.data)

        if serializer.is_valid():
            logged_in_user = request.user
            receiver = serializer.validated_data.get('receiver')
            receiver_name = receiver.name  # Assuming `name` is a field in the receiver model

            friend_request = FriendShip.objects.filter(receiver=receiver, sender=request.user).first()

            if friend_request:
                friend_request.delete()
                # return Response({'message': 'Friend request canceled successfully.'}, status=status.HTTP_204_NO_CONTENT)


                return Response({
                'status': 'success',
                'message': f"Friend request canceled successfully to {receiver_name}",
                'friend_request_id': friend_request.id,
                'receiver': receiver.id,
            }, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        users = User.objects.exclude(id=user.id)  # Exclude the current user from the list

        friend_statuses = []
        for friend in users:
            friendship = FriendShip.objects.filter(
                (Q(sender=user) & Q(receiver=friend)) | (Q(sender=friend) & Q(receiver=user))
            ).first()
            friend_id = friend.id
            friend_status = 'Friend Request Not Sent'  # Default status if no friendship exists
            friend_name = friend.name  # Get the friend's name

            # if friendship:
            #     if friendship.status == 'accepted':
            #         friend_status = 'We Are Friends'
            #     else:
            #         friend_status = 'Pending'
            # 


            if friendship:
                if friendship.sender == user and friendship.status == 'pending':
                    friend_status = 'Pending'  # Sender's profile shows "Pending"
                elif friendship.receiver == user and friendship.status == 'pending':
                    friend_status = 'Friend Request Received'  # Receiver's profile shows "Friend Request Received"
                elif friendship.status == 'accepted':
                    friend_status = 'We Are Friends'

            friend_status_data = {
                'friend_id': friend_id,
                'friend_name': friend_name,
                'friend_status': friend_status,
            }
            friend_statuses.append(friend_status_data)

   
        return Response(friend_statuses, status=status.HTTP_200_OK)    



    
    # def get_friend_status(self, user, friend_id):
    #     friendship = FriendShip.objects.filter(
    #         (Q(sender=user) & Q(receiver=friend_id)) | (Q(sender=friend_id) & Q(receiver=user))
    #     ).first()

    #     if friendship:
    #         if friendship.status == 'accepted':
    #             return 'We Are Friends'
    #         else:
    #             return 'Pending'
    #     else:
    #         return 'Friend Request Not Sent'

    # def get(self, request):
    #     user = request.user
    #     users = User.objects.exclude(id=user.id)

    #     friend_requests_with_status = []
    #     for friend in users:
    #         received_friend_request = FriendShip.objects.filter(receiver=user, sender=friend).first()
    #         sent_friend_request = FriendShip.objects.filter(sender=user, receiver=friend).first()
    #         friend_id = friend.id
    #         friend_name = friend.name

    #         if received_friend_request:
    #             friend_status = self.get_friend_status(user, friend.id)
    #         elif sent_friend_request:
    #             friend_status = 'Friend Request Sent'
    #         else:
    #             friend_status = 'Friend Request Not Sent'

    #         friend_request_data = {
    #             'friend_id': friend_id,
    #             'friend_name': friend_name,
    #             'friend_status': friend_status,
    #         }
    #         friend_requests_with_status.append(friend_request_data)

    #     return Response(friend_requests_with_status, status=status.HTTP_200_OK)


    





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

  # Create a mutual friendship by adding both users to each other's friend lists



class AcceptOrRejectFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AcceptOrRejectFriendRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            sender = serializer.validated_data.get('sender')
            
            try:
                friend_request = FriendShip.objects.get(sender=sender, receiver=request.user)
            except FriendShip.DoesNotExist:
                return Response({'message': 'Friend request does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            action = request.data.get('action')
            
            if action == 'accept':
                friend_request.accept()
                friend_request.save()
                

                
                return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.reject()
                friend_request.delete() 
                return Response({'message': 'Friend request rejected and deleted.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class AcceptOrRejectFriendRequestAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = FriendShipSerializer(data=request.data)
        
#         if serializer.is_valid():
#             receiver = serializer.validated_data.get('receiver')
            
#             try:
#                 friend_request = FriendShip.objects.get(receiver=receiver, sender=request.user)
#             except FriendShip.DoesNotExist:
#                 return Response({'message': 'Friend request does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
#             # Perform any additional checks or validations here
            
#             action = serializer.validated_data.get('action')
#             # action = request.data.get('action')
            
#             if action == 'accept':
#                 friend_request.accept()
#                 return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
#             elif action == 'reject':
#                 friend_request.reject()
#                 friend_request.delete() 

#                 return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewAllFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        friend_requests = FriendShip.objects.filter(receiver_id=user_id)
        count = FriendShip.objects.filter(receiver_id=user_id, status = 'pending').count()
        serializer = FriendRequestSerializer(friend_requests, many=True)
        serialized_data = serializer.data

        # Update serialized data to include sender's name
        for data in serialized_data:
            sender_id = data['sender']
            sender_name = User.objects.get(id=sender_id).name
            data['sender_name'] = sender_name

        if count == 0:
            return Response({'message': 'No friend requests found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'message': 'All friend requests',
            'total_friend_requests': count,
            'friend_requests': serialized_data
        }, status=status.HTTP_200_OK)

class FriendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        TotalFriend = FriendShip.objects.filter(receiver_id=user_id, status = 'accepted').count()
        result = FriendShip.objects.filter(receiver_id=user_id, status = 'accepted')
        serializer = FriendRequestSerializer(result, many=True)
        data = serializer.data
        
        if TotalFriend == 0:
            return Response({'message': 'make some founds'})

        return Response({
            'message': 'Successfull fetched list of friends',
            'total_friend': TotalFriend,
            'friend':data
        },status=status.HTTP_200_OK)

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
