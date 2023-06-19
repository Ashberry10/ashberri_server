from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
from account.serializers import UpdateUserSeriailzer, UserRegistrationSerializer,GetallUserDCsecondSeriailzer,UserLoginSeriailzer,UserProfileSerializer,GetallUserSeriailzer,UserModelSerializer,GetallUserWithCompSeriailzer
from friend.serializers import FriendShipSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from .models import UserManager,User
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
from django.conf import settings

# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.template import Context, RequestContext
import joblib
from friend.utils import get_friend_request_or_false

from rest_framework.decorators import action
import requests
# from rest_framework import generics
import json
from friend.models import FriendList, FriendShip
import os
from friend.friend_request_status import FriendRequestStatus

# from rest_framework import filters
model = joblib.load('./ABmodel.joblib')



#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
     
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = get_tokens_for_user(user)
            refresh = RefreshToken.for_user(user)

            # perser_classes = (JSONParser,FormParser,MultiPartParser)
            accessToken = str(refresh.access_token),
            # formatDate = user.date_of_birth.strftime("%d/%m/%Y")
            return Response({'accessToken':accessToken, 'msg':'Registration Successfull'},status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # @action(detail=True,method=['put'])
    # def profile(self,request,pk=None):
    #     user = self.get_object()
    #     profile = user.profile
    #     serializer = ProfileSerializer(profile,data=request.data)
    #     if serializer.is_valid:
    #         serializer.save()
    #         return Response(serializer.data,status=200)
    #     else:
    #         return Response(serializer.errors,status=400)
    
    
    
# class UserLoginView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self,request,format=None):
#         serializer = UserLoginSeriailzer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
           
#             user = authenticate(email=email,password=password)
#             if  user is not None:
#              token = get_tokens_for_user(user)
#              return Response({'token':token,'msg':'Login Successfull'},status=status.HTTP_200_OK)
#             else: 
#                 return Response({'errors':{'non_field_errors':['Email or Password-- is not Valid']}},status=status.HTTP_404_NOT_FOUND)    




class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,request,format=None):
        serializer = UserLoginSeriailzer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if  user is not None:
            #  token = get_tokens_for_user(user)
            
             refresh = RefreshToken.for_user(user)
             
             accessToken = str(refresh.access_token),
            #  name = user.name
            #  return Response({'token':token,'name':user.name,'Dfirst':user.Dfirst,'Cfirst':user.Cfirst ,'msg':'Login Successfull'},status=status.HTTP_200_OK)
             return Response({'name':user.name,'accessToken':accessToken},status=status.HTTP_200_OK)

            else: 
                return Response({'errors':{'non_field_errors':['Email or Password-- is not Valid']}},status=status.HTTP_404_NOT_FOUND)    


    


# class UserProfileView(APIView):
#     """
#     - Logic here is kind of tricky
#         is_self
#         is_friend
#             -1: NO_REQUEST_SENT
#             0: THEM_SENT_TO_YOU
#             1: YOU_SENT_TO_THEM
#     """
#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get("user_id")
#         try:
#             account = User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return Response("Account not found.", status=status.HTTP_404_NOT_FOUND)
        
#         account_serializer = UserProfileSerializer(account)
        
#         try:
#             friend_list = FriendList.objects.get(user=account)
#         except FriendList.DoesNotExist:
#             friend_list = FriendList(user=account)
#             friend_list.save()
        
#         friends = friend_list.friends.all()
#         friend_requests = None
#         user = request.user
        
#         # Define template variables
#         is_self = True
#         is_friend = False
#         request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        
#         if user.is_authenticated and user != account:
#             is_self = False
            
#             if friends.filter(pk=user.id):
#                 is_friend = True
#             else:
#                 is_friend = False
                
#                 # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
#                 if get_friend_request_or_false(sender=account, receiver=user) != False:
#                     request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
#                 # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
#                 elif get_friend_request_or_false(sender=user, receiver=account) != False:
#                     request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
#                 # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
#                 else:
#                     request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        
#         elif not user.is_authenticated:
#             is_self = False
        
#         else:
#             try:
#                 friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
#             except FriendRequest.DoesNotExist:
#                 pass
        
#         account_data = account_serializer.data
#         friend_requests_serializer = FriendRequestSerializer(friend_requests, many=True)
        
#         response_data = {
#             'account': account_data,
#             'is_self': is_self,
#             'is_friend': is_friend,
#             'request_sent': request_sent,
#             'friend_requests': friend_requests_serializer.data,
#             'BASE_URL': settings.BASE_URL
#         }
        
#         return Response(response_data, status=status.HTTP_200_OK)



# class  UserProfileView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]        
#     def get(self, request, format=None):
#         serializer = UserProfileSerializer(request.user)
#         # json_data = JSONRenderer().render(serializer.data)
#         return Response(serializer.data,content_type ='application/json')


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)

        friend_requests = FriendShip.objects.filter(receiver=user)
        friend_requests_serializer = FriendShipSerializer(friend_requests, many=True)

        friend_requests_data = []
        for friend_request in friend_requests:
            sender_data = {
                'id': friend_request.sender.id,
                'name': friend_request.sender.name,  # Assuming the sender model has a "name" field
            }
            friend_requests_data.append(sender_data)

        response_data = {
            'user_profile': serializer.data,
            'friend_requests': friend_requests_data
        }

        return Response(response_data)
# class UserChangePassword(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         serializer = UserChangePasswordSeriailzer(data=request.data,context = {'user':request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class SendPasswordResetEmailView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self,request,format=None):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({'msg':'Password Reset link send.Please check your Email'},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
# class UserPasswordResetView(APIView):
#       renderer_classes = [UserRenderer]
#       def post(self, request, uid, token, format=None):
#        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#        serializer.is_valid(raise_exception=True)
      
#        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  




class AllUser(APIView): 
    def get(self, request, *args,**kwargs):
     try:
        id = request.query_params["id"]
        if id is not None:
         stu = User.objects.get(id=id)
         serializer =  GetallUserSeriailzer(stu)
         json_data = JSONRenderer().render(serializer.data)
         return HttpResponse(json_data,content_type ='application/json')


     except:

      stu = User.objects.all()
      serializer = GetallUserSeriailzer(stu,many=True)
      json_data = JSONRenderer().render(serializer.data)
      return HttpResponse(json_data,content_type ='application/json')




class UpdateUser(APIView):
   def patch(self, request):               #update user profile 
      user = request.user                  #user refer to the loged in user (token)
      serializer = UpdateUserSeriailzer(user, data=request.data, partial = True)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# delete api

class UserDeleteView(APIView):
    def delete(self, request, id):
        try:
            id = request.query_params["id"]
            user = User.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'},status=status.HTTP_404_NOT_FOUND)




#get all user with comp (after login then this route will be accessiable)
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









