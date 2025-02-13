from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserProfileSerializer,GetallUserSeriailzer
from django.db.models import Q
from django.http import JsonResponse
from .models import User
from rest_framework.renderers import JSONRenderer
from friend.models import FriendShip
from rest_framework.permissions import IsAuthenticated
import joblib
import json
import csv

# model = joblib.load('./new_model.joblib')


# Alluser FriendStatusAndrankAPI
# class AllUser(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         logged_in_user = request.user
#         logged_in_serializer = UserProfileSerializer(logged_in_user)
#         logged_in_user_name = logged_in_serializer.data['name']
#         logged_in_user_id = logged_in_serializer.data['id']
#         logged_in_user_file = logged_in_serializer.data['file']

#         c_first = logged_in_serializer.data['C_second']
#         d_first = logged_in_serializer.data['D_second']
#         list_of_users = User.objects.exclude(id=logged_in_user.id)  # Exclude the logged-in user from the queryset
#         list_of_users_serializer = GetallUserSeriailzer(list_of_users, many=True)
#         json_data = JSONRenderer().render(list_of_users_serializer.data)
#         users_data = json.loads(json_data)

#         result = []

#         for user_data in users_data:
#             result_item = {}
#             d_second = user_data['D_second']
#             c_second = user_data['C_second']
#             friend_name = user_data['name']
#             id = user_data['id']
#             friend_file = user_data['file']

#             # Get friend status for the current user in the loop
#             friend_status = self.get_friend_status(logged_in_user, id)

#             # Your model.predict code here
#             prediction = model.predict([[d_first,c_first,c_second,d_second]])

#             result_item.update({'id': id})
#             if logged_in_user_name != friend_name:
#                 result_item.update({'ProfileName': friend_name})
#                 result_item.update({'image': friend_file})
#             if logged_in_user_name != friend_name:
#                 result_item.update({'rank': self.get_rank_label(prediction)})
#             result_item.update({'friend_status': friend_status})  # Add friend status to the result

#             result.append(result_item)

#         # Add logged-in user's profile
#         result_item = {}
#         result_item.update({'id': logged_in_user_id})
#         result_item.update({'ProfileName': logged_in_user_name})
#         result_item.update({'image': logged_in_user_file})
#         result_item.update({'rank': 'Self'})
#         result.append(result_item)

#         return JsonResponse(result, safe=False)

#     def get_rank_label(self, prediction):
#         if prediction == 0:
#             return 0
#         elif prediction[0] == 3:
#             return 3
#         elif prediction[0] == 4:
#             return 4
#         elif prediction[0] == 5:
#             return 5

#     def get_friend_status(self, user, friend_id):
#         friendship = FriendShip.objects.filter(
#             (Q(sender=user) & Q(receiver=friend_id)) | (Q(sender=friend_id) & Q(receiver=user))
#         ).first()

#         friend_status = 'Friend Request Not Sent'

#         if friendship:
#             if friendship.sender == user and friendship.status == 'pending':
#                 friend_status = 'Pending'
#             elif friendship.receiver == user and friendship.status == 'pending':
#                 friend_status = 'Friend Request Received'
#             elif friendship.status == 'accepted':
#                 friend_status = 'We Are Friends'

#         return friend_status




# # API FOR GET FriendStatusAndrnak By Id
# class FriendStatusAndrankById(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         id = request.query_params.get('id')

#         if id:
#             return self.get_friend_status_and_rank_by_id(request, id)
#         else:
#             return Response({'error': 'Missing User ID.'}, status=status.HTTP_400_BAD_REQUEST)

#     def get_friend_status_and_rank_by_id(self, request, id):
#         try:
#             friend = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         loged_in_user = request.user
#         logged_in_serializer = UserProfileSerializer(loged_in_user)
#         logged_in_user_name = logged_in_serializer.data['name']
#         c_first = logged_in_serializer.data['C_second']
#         d_first = logged_in_serializer.data['D_second']
#         logged_in_user_id = logged_in_serializer.data['id']
#         friend_serializer = UserProfileSerializer(friend)
#         friend_name = friend_serializer.data['name']
#         friend_image = friend_serializer.data['file']
#         loged_in_user_image = logged_in_serializer.data['file']

#         result = []
#         prediction = model.predict([[d_first, c_first, friend_serializer.data['C_second'], friend_serializer.data['D_second']]])

#         friend_status = self.get_friend_status(loged_in_user, friend.id)

#         if logged_in_user_id != friend.id: 
#             result_item = {}
#             result_item.update({'profileName': friend_name})
#             result_item.update({'image': friend_image})
#             result_item.update({'friend_status': friend_status})
#             result_item.update({'rank': self.get_rank_label(prediction)})


#             result.append(result_item)
#         else:
#             result_item = {}
#             result_item.update({'id': logged_in_user_id})
#             result_item.update({'profileName': logged_in_user_name})
#             result_item.update({'image': loged_in_user_image})
#             result.append(result_item)
            
#         return JsonResponse(result, safe=False)


#     def get_friend_status(self, user,id):


#        friendship = FriendShip.objects.filter(
#             (Q(sender=user) & Q(receiver=id)) | (Q(sender=id) & Q(receiver=user))
#         ).first()
 
#        friend_status = 'Friend Request Not Sent'  # Default status if no friendship exists

#        if friendship:
#             if friendship.sender == user and friendship.status == 'pending':
#                 friend_status = 'Pending'
#             elif friendship.receiver == user and friendship.status == 'pending':
#                 friend_status = 'Friend Request Received'
#             elif friendship.status == 'accepted':
#                 friend_status = 'We Are Friends'

#        return friend_status
    
    
#     def get_rank_label(self, prediction):
#         if prediction == 0:
#             return 0
#         elif prediction[0] == 3:
#             return 3
#         elif prediction[0] == 4:
#             return 4
#         elif prediction[0] == 5:
#             return 5
















# without ml model code


# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from account.serializers import UserProfileSerializer,GetallUserSeriailzer
# from django.db.models import Q
# from django.http import JsonResponse
# from .models import User
# from rest_framework.renderers import JSONRenderer
# from friend.models import FriendShip
# from rest_framework.permissions import IsAuthenticated
# import json
# import csv
# import pickle


# Build index from CSV
# def build_index_from_csv(file_path):
#     index = {}
#     with open(file_path, mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             key = (int(row['Dfirst']), int(row['Cfirst']), int(row['Csecond']), int(row['Dsecond']))
#             index[key] = int(row['rank'])
#     return index

# # Load CSV data and create the index
# csv_file_path = r"./ab_rank_rating_data.csv"
#  # Path to your CSV file
# index = build_index_from_csv(csv_file_path)

# # Save index for future use (optional)
# with open("rank_index.pkl", 'wb') as file:
#     pickle.dump(index, file)

# # Predict rank rank
# def predict_rank(Dfirst, Cfirst, Csecond, Dsecond, index):
#     key = (Dfirst, Cfirst, Csecond, Dsecond)
#     return index.get(key, "No matching data found")

# # API for getting all users and friend status with rank
# class AllUser(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         logged_in_user = request.user
#         logged_in_serializer = UserProfileSerializer(logged_in_user)
#         logged_in_user_name = logged_in_serializer.data['name']
#         logged_in_user_id = logged_in_serializer.data['id']
#         logged_in_user_file = logged_in_serializer.data['file']

#         c_first = int(logged_in_serializer.data['C_second'])
#         d_first = int(logged_in_serializer.data['D_second'])
#         list_of_users = User.objects.exclude(id=logged_in_user.id)  # Exclude the logged-in user from the queryset
#         list_of_users_serializer = GetallUserSeriailzer(list_of_users, many=True)
#         json_data = JSONRenderer().render(list_of_users_serializer.data)
#         users_data = json.loads(json_data)

#         result = []

#         for user_data in users_data:
#             result_item = {}
#             d_second = int(user_data['D_second'])
#             c_second = int(user_data['C_second'])
#             friend_name = user_data['name']
#             friend_id = user_data['id']
#             friend_file = user_data['file']

#             # Get friend status for the current user in the loop
#             friend_status = self.get_friend_status(logged_in_user, friend_id)

#             # Predict rank using CSV data
#             prediction = predict_rank(d_first, c_first, c_second, d_second, index)

#             result_item.update({'id': friend_id})
#             result_item.update({'ProfileName': friend_name})
#             result_item.update({'image': friend_file})
#             result_item.update({'rank': prediction})
#             result_item.update({'friend_status': friend_status})  # Add friend status to the result

#             result.append(result_item)

#         # Add logged-in user's profile
#         result_item = {}
#         result_item.update({'id': logged_in_user_id})
#         result_item.update({'ProfileName': logged_in_user_name})
#         result_item.update({'image': logged_in_user_file})
#         result_item.update({'rank': 'Self'})
#         result.append(result_item)

#         return JsonResponse(result, safe=False)

#     def get_friend_status(self, user, friend_id):
#         friendship = FriendShip.objects.filter(
#             (Q(sender=user) & Q(receiver=friend_id)) | (Q(sender=friend_id) & Q(receiver=user))
#         ).first()

#         friend_status = 'Friend Request Not Sent'

#         if friendship:
#             if friendship.sender == user and friendship.status == 'pending':
#                 friend_status = 'Pending'
#             elif friendship.receiver == user and friendship.status == 'pending':
#                 friend_status = 'Friend Request Received'
#             elif friendship.status == 'accepted':
#                 friend_status = 'We Are Friends'

#         return friend_status






# class FriendStatusAndrankById(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         # Get user ID from query parameters
#         id = request.query_params.get('id')

#         if id:
#             try:
#                 # Retrieve user based on ID
#                 target_user = User.objects.get(id=id)
#             except User.DoesNotExist:
#                 return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#             # Get the logged-in user information
#             logged_in_user = request.user
#             logged_in_serializer = UserProfileSerializer(logged_in_user)
#             logged_in_user_name = logged_in_serializer.data['name']
#             logged_in_user_id = logged_in_serializer.data['id']
#             logged_in_user_file = logged_in_serializer.data['file']
#             c_first = int(logged_in_serializer.data['C_second'])
#             d_first = int(logged_in_serializer.data['D_second'])

#             # Get the target user data
#             target_user_serializer = UserProfileSerializer(target_user)
#             target_user_name = target_user_serializer.data['name']
#             target_user_file = target_user_serializer.data['file']
#             c_second = int(target_user_serializer.data['C_second'])
#             d_second = int(target_user_serializer.data['D_second'])

#             # Get the friendship status
#             friend_status = self.get_friend_status(logged_in_user, target_user.id)

#             # Predict rank rank using CSV data
#             prediction = predict_rank(d_first, c_first, c_second, d_second, index)

#             result = []

#             # If the logged-in user is not the same as the target user, return rank data
#             if logged_in_user_id != target_user.id:
#                 result_item = {
#                     'id': target_user.id,
#                     'ProfileName': target_user_name,
#                     'image': target_user_file,
#                     'rank': prediction,
#                     'friend_status': friend_status
#                 }
#                 result.append(result_item)
#             else:
#                 # Return self-profile if the logged-in user matches the target user
#                 result_item = {
#                     'id': logged_in_user_id,
#                     'ProfileName': logged_in_user_name,
#                     'image': logged_in_user_file,
#                     'rank': 'Self'
#                 }
#                 result.append(result_item)

#             return JsonResponse(result, safe=False)
#         else:
#             return Response({'error': 'Missing User ID.'}, status=status.HTTP_400_BAD_REQUEST)

#     def get_friend_status(self, user, friend_id):
#         # Check for friendship status between the logged-in user and the target user
#         friendship = FriendShip.objects.filter(
#             (Q(sender=user) & Q(receiver=friend_id)) | (Q(sender=friend_id) & Q(receiver=user))
#         ).first()

#         # Default to 'Friend Request Not Sent'
#         friend_status = 'Friend Request Not Sent'

#         if friendship:
#             if friendship.sender == user and friendship.status == 'pending':
#                 friend_status = 'Pending'
#             elif friendship.receiver == user and friendship.status == 'pending':
#                 friend_status = 'Friend Request Received'
#             elif friendship.status == 'accepted':
#                 friend_status = 'We Are Friends'

#         return friend_status





# simple and with code version


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


csv_file_path = "./data.csv"
pickle_file_path = "./index.pkl"  # Path to save the Pickle file

# Load index from Pickle or build from CSV if not found
if os.path.exists(pickle_file_path):
    with open(pickle_file_path, 'rb') as pickle_file:
        index = pickle.load(pickle_file)
    print("Index loaded from Pickle file.")
else:
    index = {}
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    key = tuple(map(int, (row['Dfirst'], row['Cfirst'], row['Csecond'], row['Dsecond'])))
                    index[key] = int(row['rank'])
                except ValueError as e:
                    print(f"Skipping invalid row: {row} (Error: {e})")
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(index, pickle_file)
        print("Index built from CSV and saved to Pickle file.")
    else:
        raise FileNotFoundError(f"CSV file at {csv_file_path} not found.")

# Predict rank rank based on the index
def predict_rank(Dfirst, Cfirst, Csecond, Dsecond):
    return index.get((Dfirst, Cfirst, Csecond, Dsecond), "No matching data found")

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
            'rank': predict_rank(d_first, c_first, int(user['C_second']), int(user['D_second'])),
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
            'rank': predict_rank(d_first, c_first, c_second, d_second),
            'friend_status': get_friend_status(logged_in_user, target_user.id)
        }

        if logged_in_user.id == target_user.id:
            result['rank'] = 'Self'

        return JsonResponse([result], safe=False)
