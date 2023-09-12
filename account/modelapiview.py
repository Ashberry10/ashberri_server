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
model = joblib.load('./ABmodel.joblib')


# Alluser FriendStatusAndCompatibilityAPI
class AllUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logged_in_user = request.user
        logged_in_serializer = UserProfileSerializer(logged_in_user)
        logged_in_user_name = logged_in_serializer.data['name']
        logged_in_user_id = logged_in_serializer.data['id']
        logged_in_user_file = logged_in_serializer.data['file']

        c_first = logged_in_serializer.data['C_second']
        d_first = logged_in_serializer.data['D_second']
        list_of_users = User.objects.exclude(id=logged_in_user.id)  # Exclude the logged-in user from the queryset
        list_of_users_serializer = GetallUserSeriailzer(list_of_users, many=True)
        json_data = JSONRenderer().render(list_of_users_serializer.data)
        users_data = json.loads(json_data)

        result = []



        for user_data in users_data:
            result_item = {}
            d_second = user_data['D_second']
            c_second = user_data['C_second']
            friend_name = user_data['name']
            id = user_data['id']
            friend_file = user_data['file']

            prediction = model.predict([[d_first, c_first, c_second, d_second]])

            result_item.update({'id': id})
            if logged_in_user_name != friend_name:  # Only include friend name if it is not the logged-in user
                # result_item.update({'FriendName': friend_name})
                result_item.update({'ProfileName': friend_name})
                result_item.update({'image': friend_file})
            if logged_in_user_name != friend_name:  # Only include compatibility if it is not the logged-in user
                result_item.update({'Compatibility': self.get_compatibility_label(prediction)})


            result.append(result_item)



                # Add logged-in user's profile
        result_item = {}
        # id = user_data['id']
        result_item.update({'id': logged_in_user_id})
        result_item.update({'ProfileName': logged_in_user_name})
        result_item.update({'image': logged_in_user_file})
        # result_item.update({'FriendName': logged_in_user_name})
        result_item.update({'Compatibility': 'Self'})  # Indicate it's the logged-in user
        result.append(result_item)
        return JsonResponse(result, safe=False)



    def get_compatibility_label(self, prediction):
        if prediction == 0:
            return 0
        elif prediction[0] == 3:
            return 3
        elif prediction[0] == 4:
            return 4
        elif prediction[0] == 5:
            return 5


# API FOR GET FriendStatusAndCompatibilit By Id
class FriendStatusAndCompatibilityById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        # id = request.data.get('id')

        if id:
            return self.get_friend_status_and_compatibility_by_id(request, id)
        else:
            return Response({'error': 'Missing User ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_friend_status_and_compatibility_by_id(self, request, id):
        try:
            friend = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        loged_in_user = request.user
        logged_in_serializer = UserProfileSerializer(loged_in_user)
        logged_in_user_name = logged_in_serializer.data['name']
        c_first = logged_in_serializer.data['C_second']
        d_first = logged_in_serializer.data['D_second']
        logged_in_user_id = logged_in_serializer.data['id']
        friend_serializer = UserProfileSerializer(friend)
        friend_name = friend_serializer.data['name']
        friend_image = friend_serializer.data['file']
        result = []
        prediction = model.predict([[d_first, c_first, friend_serializer.data['C_second'], friend_serializer.data['D_second']]])

        friend_status = self.get_friend_status(loged_in_user, friend.id)
        
        if logged_in_user_id != friend.id:
            result_item = {}
            result_item.update({'profileName': friend_name})
            result_item.update({'image': friend_image})
            result_item.update({'friendStatus': friend_status})
            result_item.update({'compatibility': self.get_compatibility_label(prediction)})


            result.append(result_item)
        else:
            result_item = {}
            result_item.update({'id': logged_in_user_id})
            result_item.update({'ProfileName': logged_in_user_name})
            result.append(result_item)
            
        return JsonResponse(result, safe=False)

    def get_friend_status(self, user, id):
        friendship = FriendShip.objects.filter(
            (Q(sender=user) & Q(receiver=id)) | (Q(sender=id) & Q(receiver=user))
        ).first()

        if friendship:
            if friendship.status == 'accepted':
                return 'We Are Friends'
            else:
                return 'Pending'
        else:
            return 'Friend Request Not Sent'

    def get_compatibility_label(self, prediction):
        if prediction == 0:
            return 0
        elif prediction[0] == 3:
            return 3
        elif prediction[0] == 4:
            return 4
        elif prediction[0] == 5:
            return 5
