from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,GetallUserDCsecondSeriailzer,UserLoginSeriailzer,UserProfileSerializer,GetallUserSeriailzer,UserModelSerializer,GetallUserWithCompSeriailzer
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
            user= serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successfull'},status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
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
             token = get_tokens_for_user(user)
            #  name = user.name
            #  return Response({'token':token,'name':user.name,'Dfirst':user.Dfirst,'Cfirst':user.Cfirst ,'msg':'Login Successfull'},status=status.HTTP_200_OK)
             return Response({'name':user.name,'token':token},status=status.HTTP_200_OK)

            else: 
                return Response({'errors':{'non_field_errors':['Email or Password-- is not Valid']}},status=status.HTTP_404_NOT_FOUND)    



# # AB model api
# class ModelapiView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]        
#     def get(self, request, format=None):
#         serializer = UserProfileSerializer(request.user)
#         # D_first = request.data['D_first']
#         # C_first = request.data['C_first'] 
#         # C_second = request.data['C_second'] 
#         # D_second = request.data['D_second'] 
#        # model = joblib.load(os.path.join('./ABmodel.joblib'))
#         # p rediction = model.predict([[D_first, C_first, C_second, D_second]])
#         # prediction = model.predict([[1, 1, 1, 1]])

#         # if (prediction == 0) :
#         #     predicted_class = 'Not friend'
#         # elif prediction[0] == 3:
#         #      predicted_class = '* * *'
#         # elif prediction[0] == 4:
#         #      predicted_class = '* * * *'    
#         # elif prediction[0] == 5:
#         #      predicted_class = '* * * * *' 
#         return Response("dssdf",serializer.data)
           
class  UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]        
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)







# def courseDetails(request,courseid):

#      r = requests.get('http://127.0.0.1:8000/api/user/getallusers/')
#      return Response(r)







class band_listing(APIView):
    
    def post(self,request):
        """A view of all bands."""
  
        name = request.GET.get('name')
        roll  = request.GET.get('roll')
 
        # template = "base/home.html"
        context ={
           'name':name,
          'roll':roll
          }


        # r = requests.get('http://127.0.0.1:8000/api/user/getallusers/')
        return Response(context) 
        # return Response(r) 

    
    
    


# def band_listing(request):
#     """A view of all bands."""
#     # bands = Band.objects.all()
#     name = request.GET.get('name')
#     roll  = request.GET.get('roll')
 
#     template = "base/home.html"
#     context ={
#         'name':name,
#         'roll':roll
#     }
    
    
    
#     # return render(request, template,context)
      


      





class ModelapiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):

        # 1 geting the data from the loged in user
        LogedInserializer = UserProfileSerializer(request.user)
        LogedInUserName = LogedInserializer.data['name']
        LogedInUseremail = LogedInserializer.data['email']
        LogedInUserCfirst = LogedInserializer.data['C_second']
        LogedInUserDfirst = LogedInserializer.data['D_second']

        print(LogedInUserName)
        print(LogedInUseremail)
        print(LogedInUserCfirst)
        print(LogedInUserDfirst)

        # 2 list of user from the database
        listofuser = User.objects.values('D_second','C_second')
        listofuserSerializer = GetallUserDCsecondSeriailzer(listofuser,many=True)

        #print(listofuserSerializer.data)      
    # obj = [OrderedDict([('email', 'admin@example.com'), ('name', 'Admin kumar'), ('D_second', 0), ('C_second', 0)]), 
    #    OrderedDict([('email', 'pc@gmail.com'), ('name', 'pc'), ('D_second', 0), ('C_second', 0)]),
    #    OrderedDict([('email', 'pc23@gmail.com'), ('name', 'pc23'), ('D_second', 0), ('C_second', 0)]),
    #    OrderedDict([('email', 'sdfsd@gmail.co'),('name', 'dsfs'), ('D_second', 0), ('C_second', 0)]),
    #    OrderedDict([('email', 'ram3@gmail.com'), ('name', 'ram'), ('D_second', 0), ('C_second', 0)]),
    #    OrderedDict([('email', 'rasddm23@gmail.com'), ('name', 'sdf'), ('D_second', 0), ('C_second', 0)]),
    #    OrderedDict([('email', 'sam23@gmail.com'), ('name', 'sam'), ('D_second', 4), ('C_second', 3)])]
      
        # obdf =  {"sdf":23,"sdfd":23}
        # print (obdf.keys())
        json_data = JSONRenderer().render(listofuserSerializer.data)
        # print(json_data)

        # print(type(json_data))


        res_dict = json.loads(json_data)
        # printing type and list
        # print(type(res_dict))
        print(res_dict)

        

        # b'[{"email":"admin@example.com","name":"Admin kumar","D_second":0,"C_second":0},
        # {"email":"pc@gmail.com","name":"pc","D_second":0,"C_second":0},
        # {"email":"pc23@gmail.com","name":"pc23","D_second":0,"C_second":0},
        # {"email":"sdfsd@gmail.co","name":"dsfs","D_second":0,"C_second":0},
        # {"email":"ram3@gmail.com","name":"ram","D_second":0,"C_second":0},
        # {"email":"rasddm23@gmail.com","name":"sdf","D_second":0,"C_second":0},
        # {"email":"sam23@gmail.com","name":"sam","D_second":4,"C_second":3}]'
      
        # updated and converted to list datatype
        #print(str(res_dict))
        #[{'email': 'admin@example.com', 'name': 'Admin kumar', 'D_second': 0, 'C_second': 0}, {'email': 'pc@gmail.com', 'name': 'pc', 'D_second': 0, 'C_second': 0}, {'email': 'pc23@gmail.com', 'name': 'pc23', 'D_second': 0, 'C_second': 0}, {'email': 'sdfsd@gmail.co', 'name': 'dsfs', 'D_second': 0, 'C_second': 0}, {'email': 'ram3@gmail.com', 'name': 'ram', 'D_second': 0, 'C_second': 0}, {'email': 'rasddm23@gmail.com', 'name': 'sdf', 'D_second': 0, 'C_second': 0}, {'email': 'sam23@gmail.com', 'name': 'sam', 'D_second': 4, 'C_second': 3}]
       
        #3
        #print the individual element of json_data ?
        print("individual elements")
   

        print("key and values of D and C")
   
        # print(str(sdfsd.get("email")))
        # print(str(res_dict[1].D_second))
        # for user in res_dict:
        #     print(user)
        #print(res_dict)
        #map method 
        # len = map(json_data,["name"])
        # print(len)

        
        

        return Response(status=status.HTTP_200_OK)

    
    


    
    
    




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
      stu = User.objects.all()
      serializer = GetallUserSeriailzer(stu,many=True)
      json_data = JSONRenderer().render(serializer.data)
      return HttpResponse(json_data,content_type ='application/json')






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














