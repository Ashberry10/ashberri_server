from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserProfileSerializer,GetallUserSeriailzer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q

from django.http import JsonResponse
from .models import UserManager,User
from rest_framework.renderers import JSONRenderer
from friend.models import FriendShip
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.template import Context, RequestContext
import joblib
import requests
# from rest_framework import generics
import json
import os
# from rest_framework import filters
model = joblib.load('./ABmodel.joblib')








# Note:- DCsecond for login user and  all the user 
# but in function we are making CDfirst for login and  
# CDsecond for other user except loged in one ,in such  
# a way that we can make successfull pridiction



# class ModelapiView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, format=None):
         
   
      
#       try:
#          id = request.query_params["id"]
#          if id is not None:
#             # 1 geting the data from the loged in user


#           LogedInserializer = UserProfileSerializer(request.user)
#           LogedInUserName = LogedInserializer.data['name']

#           C_first = LogedInserializer.data['C_second']
#           D_first = LogedInserializer.data['D_second']
#           stu = User.objects.get(id=id)
#           serializer =  UserProfileSerializer(stu)
#           json_data = JSONRenderer().render(serializer.data)
#           res_dict = json.loads(json_data)

          
          
          
#           D_second = res_dict['D_second']
#           C_second = res_dict['C_second']
#           friendname = res_dict['name']  
       
#         #   print("yourfriendName",friendname)
#         #   print("dfisrt_for_logedin",D_first)
#         #   print("cfisrt_for_logedin",C_first)
#         #   print("dsecond_your_friend",D_second)
#         #   print("csecond_your_friend",C_second)



#          Response = []
#          model = joblib.load(os.path.join('./ABmodel.joblib'))

#          Result = {} #dictinory   
   
        
  
#          prediction = model.predict([[D_first, C_first, C_second, D_second]])

#          if (prediction == 0) :
#              predicted_class = 'Not friend'
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
            
#              Result.update({'Compatibility': predicted_class})  

#          elif prediction[0] == 3:
#              predicted_class = '* * *'
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class}) 
#          elif prediction[0] == 4:
#              predicted_class = '* * * *'  
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class}) 
 
#          elif prediction[0] == 5:
#              predicted_class = '* * * * *'
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class})   
#          Response.append(Result) 

#          return JsonResponse(
#             Response,safe=False
#          )                                          
                                      


#       except:
#         LogedInserializer = UserProfileSerializer(request.user)
#         LogedInUserName = LogedInserializer.data['name']
#         LogedInUseremail = LogedInserializer.data['email']
#         C_first = LogedInserializer.data['C_second']
#         D_first = LogedInserializer.data['D_second']

#         # 2 list of user from the database
#         listofuser = User.objects.all()
#         # listofuserSerializer = GetallUserDCsecondSeriailzer(listofuser,many=True)     # listofuser = User.objects.values('D_second','C_second')
#         listofuserSerializer = GetallUserSeriailzer(listofuser,many=True)
    
#         json_data = JSONRenderer().render(listofuserSerializer.data)
#         res_dict = json.loads(json_data) #list of all user from the database 
#         lengthofalluser = len(res_dict)
        
#         # print(LogedInUserName)
#         #3
#         #print the individual element of json_data ?
#         print("individual elements")
 

#         Response = []
#         model = joblib.load(os.path.join('./ABmodel.joblib'))


#         i = 0
#         for item in  res_dict:
#          Result = {} #dictinory   
#          second = res_dict[i] #individual user       
#          i = i+1
          
#          D_second = second['D_second']
#          C_second = second['C_second']
#          friendname = second['name']
#          id = second['id']
        
  
#          prediction = model.predict([[D_first, C_first, C_second, D_second]])

#          if (prediction == 0) :
#             predicted_class = 'Not friend'
#             Result.update({'id': id}) 
#             Result.update({'ProfileName': LogedInUserName}) 

#             Result.update({'FriendName': friendname}) 
            
#             Result.update({'Compatibility': predicted_class})  
 
#          elif prediction[0] == 3:
#              predicted_class = '* * *'
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class}) 
#          elif prediction[0] == 4:
#              predicted_class = '* * * *'  
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class}) 
 
#          elif prediction[0] == 5:
#              predicted_class = '* * * * *'
#              Result.update({'id': id}) 
#              Result.update({'ProfileName': LogedInUserName}) 

#              Result.update({'FriendName': friendname}) 
             
#              Result.update({'Compatibility': predicted_class})   
#          Response.append(Result) 
      
          
             


#         # return JsonResponse({
#         #     'Prediction': Response
#         #     # 'friend':friendname,
#         #     # 'yourname':LogedInUserName

#         #  })                          

#         return JsonResponse(
#             Response,safe=False
#          )                                           









# Alluser FriendStatusAndCompatibilityAPI
class FriendStatusAndCompatibility(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        loged_in_user = request.user
        loged_in_serializer = UserProfileSerializer(loged_in_user)
        loged_in_user_name = loged_in_serializer.data['name']
        c_first = loged_in_serializer.data['C_second']
        d_first = loged_in_serializer.data['D_second']

        list_of_users = User.objects.all()
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

            prediction = model.predict([[d_first, c_first, c_second, d_second]])

            friend_status = self.get_friend_status(loged_in_user, id)

            result_item.update({'id': id})
            result_item.update({'ProfileName': loged_in_user_name})
            result_item.update({'FriendName': friend_name})
            result_item.update({'FriendStatus': friend_status})
            result_item.update({'Compatibility': self.get_compatibility_label(prediction)})

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
            return 'Not Friend'
        elif prediction[0] == 3:
            return '* * *'
        elif prediction[0] == 4:
            return '* * * *'
        elif prediction[0] == 5:
            return '* * * * *'








# API FOR GET FriendStatusAndCompatibilit By Id

class FriendStatusAndCompatibilityById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        # id = request.data.get('id')
        
        if id:
            return self.get_friend_status_and_compatibility_by_id(request, id)
        else:
            return self.get_all_friend_status_and_compatibility(request)
        
    def get_all_friend_status_and_compatibility(self, request):
        loged_in_user = request.user
        loged_in_serializer = UserProfileSerializer(loged_in_user)
        loged_in_user_name = loged_in_serializer.data['name']
        c_first = loged_in_serializer.data['C_second']
        d_first = loged_in_serializer.data['D_second']

        list_of_users = User.objects.all()
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

            prediction = model.predict([[d_first, c_first, c_second, d_second]])

            friend_status = self.get_friend_status(loged_in_user, id)

            result_item.update({'id': id})
            result_item.update({'ProfileName': loged_in_user_name})
            result_item.update({'FriendName': friend_name})
            result_item.update({'FriendStatus': friend_status})
            result_item.update({'Compatibility': self.get_compatibility_label(prediction)})

            result.append(result_item)

        return JsonResponse(result, safe=False)

    def get_friend_status_and_compatibility_by_id(self, request, id):
        try:
            friend = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'Friend does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        loged_in_user = request.user
        loged_in_serializer = UserProfileSerializer(loged_in_user)
        loged_in_user_name = loged_in_serializer.data['name']
        c_first = loged_in_serializer.data['C_second']
        d_first = loged_in_serializer.data['D_second']

        friend_serializer = UserProfileSerializer(friend)
        friend_name = friend_serializer.data['name']
        result = []
        prediction = model.predict([[d_first, c_first, friend_serializer.data['C_second'], friend_serializer.data['D_second']]])

        friend_status = self.get_friend_status(loged_in_user, friend.id)
        result_item = {}
        result_item.update({'id': id})
        result_item.update({'ProfileName': loged_in_user_name})
        result_item.update({'FriendName': friend_name})
        result_item.update({'FriendStatus': friend_status})
        result_item.update({'Compatibility': self.get_compatibility_label(prediction)})

      
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
            return 'Not Friend'
        elif prediction[0] == 3:
            return '* * *'
        elif prediction[0] == 4:
            return '* * * *'
        elif prediction[0] == 5:
            return '* * * * *'





























# API FOR BOTH GETUSERID AND ALLUSER FriendStatusAndCompatibility
# class FriendStatusAndCompatibilityAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         id = request.query_params.get('id')
#         if id:
#             return self.get_friend_status_and_compatibility_by_id(request, id)
#         else:
#             return self.get_friend_status_and_compatibility(request)

#     def get_friend_status_and_compatibility(self, request):
#         loged_in_user = request.user
#         loged_in_serializer = UserProfileSerializer(loged_in_user)
#         loged_in_user_name = loged_in_serializer.data['name']
#         c_first = loged_in_serializer.data['C_second']
#         d_first = loged_in_serializer.data['D_second']

#         list_of_users = User.objects.all()
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

#             prediction = self.get_prediction(d_first, c_first, c_second, d_second)

#             friend_status = self.get_friend_status(loged_in_user, id)

#             result_item.update({'id': id})
#             result_item.update({'ProfileName': loged_in_user_name})
#             result_item.update({'FriendName': friend_name})
#             result_item.update({'FriendStatus': friend_status})
#             result_item.update({'Compatibility': self.get_compatibility_label(prediction)})

#             result.append(result_item)

#         return JsonResponse(result, safe=False)

#     def get_friend_status_and_compatibility_by_id(self, request, id):
#         try:
#             friend = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return Response({'error': 'Friend does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         loged_in_user = request.user
#         loged_in_serializer = UserProfileSerializer(loged_in_user)
#         loged_in_user_name = loged_in_serializer.data['name']
#         c_first = loged_in_serializer.data['C_second']
#         d_first = loged_in_serializer.data['D_second']

#         friend_serializer = UserProfileSerializer(friend)
#         friend_name = friend_serializer.data['name']

#         prediction = self.get_prediction(d_first, c_first, friend_serializer.data['C_second'], friend_serializer.data['D_second'])

#         friend_status = self.get_friend_status(loged_in_user, friend.id)

#         response_data = {
#             'id': id,
#             'ProfileName': loged_in_user_name,
#             'FriendName': friend_name,
#             'FriendStatus': friend_status,
#             'Compatibility': self.get_compatibility_label(prediction)
#         }

#         return JsonResponse(response_data)

#     def get_friend_status(self, user, id):
#         friendship = FriendShip.objects.filter(
#             (Q(sender=user) & Q(receiver=id)) | (Q(sender=id) & Q(receiver=user))
#         ).first()

#         if friendship:
#             if friendship.status == 'accepted':
#                 return 'We Are Friends'
#             else:
#                 return 'Pending'
#         else:
#             return 'Friend Request Not Sent'

#     def get_prediction(self, d_first, c_first, c_second, d_second):
#         return model.predict([[d_first, c_first, c_second, d_second]])

#     def get_compatibility_label(self, prediction):
#         if prediction == 0:
#             return 'Not Friend'
#         elif prediction[0] == 3:
#             return '* * *'
#         elif prediction[0] == 4:
#             return '* * * *'
#         elif prediction[0] == 5:
#             return '* * * * *'









