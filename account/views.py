from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSeriailzer,UserProfileSerializer,GetallUserSeriailzer
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
from django.shortcuts import render
from django.template import Context, RequestContext
import joblib
import requests
import os
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







# AB model api
class ModelapiView(APIView):
    
    # def get(self, request):

    #     return JsonResponse({"key": "Hello World"})
		
    def post(self, request):
	
        # D_first = request.GET.get['D_first']
        # C_first = request.GET.get['C_first'] 
        # C_second = request.GET.get['C_second'] 
        # D_second = request.GET.get['D_second'] 

        
        
        # By passing parameter on url or params
        # D_first = 9
        D_first = request.GET.get('D_first')
        C_first = request.GET.get('C_first') 
        C_second = request.GET.get('C_second') 
        D_second = request.GET.get('D_second') 
        # r = requests.get('http://127.0.0.1:8000/api/user/getallusers/')

        # without  passing parameter on url
        # D_first = request.data['D_first']
        # C_first = request.data['C_first'] 
        # C_second = request.data['C_second'] 
        # D_second = request.data['D_second'] 



    
        #  request.GET.get('name')
        # print(os.getcwd())
        # print("Hi")
        model = joblib.load(os.path.join('./ABmodel.joblib'))
        prediction = model.predict([[D_first, C_first, C_second, D_second]])
        if (prediction == 0) :
            predicted_class = 'Not friend'
        elif prediction[0] == 3:
             predicted_class = '* * *'
        elif prediction[0] == 4:
             predicted_class = '* * * *'    
        elif prediction[0] == 5:
             predicted_class = '* * * * *' 
        
        
        # users = r.json()
        # print(r)
             
             
        return JsonResponse({
            'Prediction': predicted_class
        })



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
      


      





class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    




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
  









#get all User

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














