from rest_framework import serializers
from account.models import User, UserPost
# from xml.dom import ValidationErr
# from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util







class UserRegistrationSerializer(serializers.ModelSerializer):
      # password2 = serializers.CharField(style={'input_type':'password'},write_only =True)
      # profile = ProfileSerializer(read_only=True)
    #   class ImageSerializer(serializers.ModelSerializer):
    #     file = serializers.ImageField(
    #     max_length=None, use_url=True,
    # )
      class Meta:
        model = User
        # fields = ['email','username','password','date_of_birth'] 
        # DCsecond is calculated in the backgroud we dont need to fill dcsecind ,calculateing function are in models.py
        # file = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
        
        fields = ['email','name','password','D_second','C_second','day','month','year'] 
        # fields = ['email','name','password','D_second','C_second','day','month','year'] 


        # extra_Kwargs={
        #     'password':{'write_only':True}
        # }
        
        #Validating Password and Confirm Password while Registration
      # def validate(self,attrs):
      #       password = attrs.get('password')
            # password2 = attrs.get('password2')
            # if password != password2: 
            #     raise serializers.ValidationError("Password and Confirm Password doesn't match")
                

            # return attrs

      def create(self,validate_data):
            return User.objects.create_user(**validate_data)
            

class UserLoginSeriailzer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length= 255)
  class Meta:
    model = User
    fields = ['email','password']




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
     model = User
     fields = ['id', 'email', 'name','day','month','year','date_of_birth','D_second','C_second','file']

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
     model = User
     fields = ['id', 'email', 'name','D_second','C_second']

class GetallUserSeriailzer(serializers.ModelSerializer):
      # email = serializers.EmailField(max_length= 255)
  class Meta:
    model = User
    fields = ['id', 'email', 'name','D_second','C_second','date_of_birth','day','year','month','file']

class UpdateUserSeriailzer(serializers.ModelSerializer):
  class Meta:
    model = User
    # fields = [ 'email', 'name','day','year','month']
    file = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    fields = [ 'email', 'name','day','year','month','file']

#Post Seriailzer
class UserPostSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserPost
      fields = ['url']




# class UserChangePasswordSeriailzer(serializers.Serializer):
#    password = serializers.CharField(max_length =255, style ={'input_type':'password'},write_only=True)
#    password2 = serializers.CharField(max_length =255, style ={'input_type':'password'},write_only=True)
#    class Meta:
#         fields = ['password','password2']
   
#    def validate(self,attrs):
#       password = attrs.get('password')
#       password2 = attrs.get('password2')
#       user = self.context.get('user')
#       if password != password2: 
#           raise serializers.ValidationError("Password and Confirm Password doesn't match")
#       user.set_password(password)
#       user.save()
#       return attrs
         
       
     
# class SendPasswordResetEmailSerializer(serializers.Serializer):
#       email = serializers.EmailField(max_length=255)
#       class Meta:
#             fields =['email']
#       def validate(self, attrs):
#           email = attrs.get('email')
#           if User.objects.filter(email=email).exists():
#               user = User.objects.get(email= email)
#               uid = urlsafe_base64_encode(force_bytes(user.id))
#               print('Encoded UID',uid)
#               token  = PasswordResetTokenGenerator().make_token(user)
#               print('Password Reset Token',token)
#               link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
#               print('Password Reset Link',link)
#               #Send Email
#               body = 'Click Following Link to Reset Your Password '+link
#               data = {
#                 'subject':'Reset Your Password',
#                 'body':body,
#                 'to_email':user.email
#                }
#               # Util.send_email(data)  #to send in gmail for reset the password we need to turn on Less secure app access in gmail in which the setting is no longer available. 
#               return attrs

#           else:
#                 raise ValidationErr('You are not a Registered User')
         

# class UserPasswordResetSerializer(serializers.Serializer):
#   password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   class Meta:
#     fields = ['password', 'password2']

#   def validate(self, attrs):
#     try:
#       password = attrs.get('password')
#       password2 = attrs.get('password2')
#       uid = self.context.get('uid')
#       token = self.context.get('token')
#       if password != password2:
#         raise serializers.ValidationError("Password and Confirm Password doesn't match")
#       id = smart_str(urlsafe_base64_decode(uid))
#       user = User.objects.get(id=id)
#       if not PasswordResetTokenGenerator().check_token(user, token):
#         raise serializers.ValidationError('Token is not Valid or Expired')
#       user.set_password(password)
#       user.save()
#       return attrs
#     except DjangoUnicodeDecodeError as identifier:
#       PasswordResetTokenGenerator().check_token(user, token)
#       raise serializers.ValidationError('Token is not Valid or Expired')  

     

     


class GetallUserDCsecondSeriailzer(serializers.ModelSerializer):
      # email = serializers.EmailField(max_length= 255)
  class Meta:
    model = User
    fields = ['D_second','C_second']

class GetallUserWithCompSeriailzer(serializers.ModelSerializer):
   class Meta:
    model = User
    fields = ['name','id',]
