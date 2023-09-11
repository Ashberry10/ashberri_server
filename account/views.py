import mimetypes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UpdateUserSeriailzer, UserRegistrationSerializer, UserLoginSeriailzer, UserProfileSerializer, GetallUserSeriailzer
from friend.serializers import FriendShipSerializer
from django.contrib.auth import authenticate
from .models import User
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials
import joblib  # from django_filters.rest_framework import DjangoFilterBackend
from friend.models import FriendShip  # from rest_framework import generics
print('inside views.py')
# from rest_framework import filters
model = joblib.load('./ABmodel.joblib')

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Registration
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = get_tokens_for_user(user)
            refresh = RefreshToken.for_user(user)

            # perser_classes = (JSONParser,FormParser,MultiPartParser)
            accessToken = str(refresh.access_token),
            # formatDate = user.date_of_birth.strftime("%d/%m/%Y")
            return Response({'accessToken': accessToken, 'msg': 'Registration Successfull'}, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Loging
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSeriailzer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                #  token = get_tokens_for_user(user)

                refresh = RefreshToken.for_user(user)

                accessToken = str(refresh.access_token),
            #  name = user.name
            #  return Response({'token':token,'name':user.name,'Dfirst':user.Dfirst,'Cfirst':user.Cfirst ,'msg':'Login Successfull'},status=status.HTTP_200_OK)
                return Response({'name': user.name, 'accessToken': accessToken}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': {'non_field_errors': ['Email or Password-- is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

#User Profile
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)

        friend_requests = FriendShip.objects.filter(receiver=user)
        friend_requests_serializer = FriendShipSerializer(
            friend_requests, many=True)

        friend_requests_data = []
        for friend_request in friend_requests:
            sender_data = {
                'id': friend_request.sender.id,
                # Assuming the sender model has a "name" field
                'name': friend_request.sender.name,
            }
            friend_requests_data.append(sender_data)

        response_data = {
            'user_profile': serializer.data,
            'friend_requests': friend_requests_data
        }

        return Response(response_data)
    
    def patch(self, request):  # update user profile
        user = request.user  # user refer to the loged in user (token)
        serializer = UpdateUserSeriailzer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            stu = User.objects.get()
            print("stu: " , stu)
            serializer = GetallUserSeriailzer(stu)
            json_data = JSONRenderer().render(serializer.data)
            
            return HttpResponse(json_data, content_type='application/json')

        except:

            stu = User.objects.all()
            serializer = GetallUserSeriailzer(stu, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')


class UpdateUser(APIView):
    def patch(self, request):  # update user profile
        user = request.user  # user refer to the loged in user (token)
        serializer = UpdateUserSeriailzer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete api

class UserDeleteView(APIView):
    def delete(self, request, id):
        try:
            id = request.query_params["id"]
            user = User.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# get all user with comp (after login then this route will be accessiable)
# class AllUserwithComp(APIView):
#     # renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args,**kwargs):
#       stu = User.objects.all()
#       serializer = GetallUserWithCompSeriailzer(stu,many=True)
#       json_data = JSONRenderer().render(serializer.data)
#       return HttpResponse(json_data,content_type ='application/json')


# def go():
#     return 1+2
# #get all user with comp (after login then this route will be accessiable)
# class AllUserwithComp(APIView):

#     # renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args,**kwargs):
#       stu = User.objects.all()
#       serializer = GetallUserWithCompSeriailzer(stu,many=True)
#       sdf = go()
#       json_data = JSONRenderer().render(serializer.data)
#       return HttpResponse(json_data,sdf,content_type ='application/json')
