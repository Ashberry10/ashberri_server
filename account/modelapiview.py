


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserProfileSerializer, GetallUserSeriailzer
from django.db.models import Q
from django.http import JsonResponse
from .models import User
from friend.models import FriendShip
from rest_framework.permissions import IsAuthenticated
import json, csv, pickle
import os


# csv_file_path =
# pickle_file_path = "./index.pkl"  # Path to save the Pickle file

# # Load index from Pickle or build from CSV if not found
# if os.path.exists(pickle_file_path):
#     with open(pickle_file_path, 'rb') as pickle_file:
#         index = pickle.load(pickle_file)
#     print("Index loaded from Pickle file.")
# else:
#     index = {}
#     if os.path.exists(csv_file_path):
#         with open(csv_file_path, mode='r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     key = tuple(map(int, (row['Dfirst'], row['Cfirst'], row['Csecond'], row['Dsecond'])))
#                     index[key] = int(row['rank'])
#                 except ValueError as e:
#                     print(f"Skipping invalid row: {row} (Error: {e})")
#         with open(pickle_file_path, 'wb') as pickle_file:
#             pickle.dump(index, pickle_file)
#         print("Index built from CSV and saved to Pickle file.")
#     else:
#         raise FileNotFoundError(f"CSV file at {csv_file_path} not found.")

# # Predict rank rank based on the index
# def predict_rank(Dfirst, Cfirst, Csecond, Dsecond):
#     return index.get((Dfirst, Cfirst, Csecond, Dsecond), "No matching data found")

def get_friend_status(user, friend_id):
    friendship = FriendShip.objects.filter(Q(sender=user, receiver=friend_id) | Q(sender=friend_id, receiver=user)).first()
    if friendship:
        if friendship.status == 'pending':
            return 'Pending' if friendship.sender == user else 'Friend Request Received'
        if friendship.status == 'accepted':
            return 'We Are Friends'
    return 'Friend Request Not Sent'



class AllUserInfoWithFriendStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logged_in_user = request.user
        users_data = GetallUserSeriailzer(User.objects.exclude(id=logged_in_user.id), many=True).data
        logged_in_profile = UserProfileSerializer(logged_in_user).data
        d_first, c_first = int(logged_in_profile['D_second']), int(logged_in_profile['C_second'])

        result = [{
            'id': user['id'], 'ProfileName': user['name'], 'image': user['file'],'gender':user['gender'],'date_of_birth':user['date_of_birth'],
            # 'rank': predict_rank(d_first, c_first, int(user['C_second']), int(user['D_second'])),
            'friend_status': get_friend_status(logged_in_user, user['id'])
        } for user in users_data]

        result.append({
            'id': logged_in_user.id, 'ProfileName': logged_in_profile['name'],'gender':logged_in_profile['gender'],'date_of_birth':logged_in_profile['date_of_birth'],
            'image': logged_in_profile['file'], 'rank': 'Self'
        })
        return JsonResponse(result, safe=False)

class UserByIdInfoWithFriendStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'error': 'Missing User ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        logged_in_user = request.user
        logged_in_profile = UserProfileSerializer(logged_in_user).data
        target_profile = UserProfileSerializer(target_user).data
        d_first, c_first = int(logged_in_profile['D_second']), int(logged_in_profile['C_second'])
        d_second, c_second = int(target_profile['D_second']), int(target_profile['C_second'])

        result = {
            'id': target_user.id, 'ProfileName': target_profile['name'], 'image': target_profile['file'],'gender':target_profile['gender'],'date_of_birth':target_profile['date_of_birth'],
            # 'rank': predict_rank(d_first, c_first, c_second, d_second),
            'friend_status': get_friend_status(logged_in_user, target_user.id)
        }

        if logged_in_user.id == target_user.id:
            result['rank'] = 'Self'

        return JsonResponse([result], safe=False)
