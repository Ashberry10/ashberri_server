import mimetypes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import CommentSerializer, LikeSerializer, PostSerializer, ShareSerializer, UpdateUserSeriailzer, UserRegistrationSerializer, UserLoginSeriailzer, UserProfileSerializer, GetallUserSeriailzer
from friend.serializers import FriendShipSerializer
from django.contrib.auth import authenticate
from .models import Comment, Like, Post, Share, User
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


class CreatePost1(APIView):
    print('inside upload class')

    def post(self, request):
        try:
            print('hi inside post upload')
            print(request.data)
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                print('serializer is valid ')
                print('function call start')
                image_url = self.upload_to_firebase(request.data['image'])
                print('function call ends')
                print('image url', image_url)
                serializer.save(url=image_url)
            else:
                print('serializer is not valid')
            return Response({'message': 'Post upladed'})
        except:
            raise APIException('Error uploading the post')
# Post START


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        luser = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=luser)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)  # todo add more details in resposne

    def patch(self, request, post_id):  # update user profile
        user = post_id  # user refer to the loged in user (token)
        serializer = UpdateUserSeriailzer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            # serializer.save()
            return Response("UPDATED work in progress")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        like = Like(user=request.user, post=post)
        like.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        # post = Post.objects.filter(id=post_id)

        like = Like(user=request.user, post=post)

        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)  # todo add more details in resposne


class SharePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        share = Share(user=request.user, post=post)
        share.save()
        return Response(status=status.HTTP_201_CREATED)


class CommentPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class GetPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetLikes(APIView):
    def get(self, request, post_id):
        likes = Like.objects.filter(post_id=post_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class GetShares(APIView):
    def get(self, request, post_id):
        shares = Share.objects.filter(post_id=post_id)
        serializer = ShareSerializer(shares, many=True)
        return Response(serializer.data)


# Post END

    def get(self, request):
        image_urls = self.get_all_image_urls()
        return Response(image_urls)

    def upload_to_firebase(self, image):
        print(image)
        print('inside upload to firebase started')
        cred = credentials.Certificate('firebaseKey.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'photos-798d6.appspot.com'
        })
        print(image)
        bucket = storage.bucket()
        file_path = f'images/{image.name}'
        blob = bucket.blob(file_path)
        # Set the content type of the file based on its extension
        content_type, _ = mimetypes.guess_type(image.name)
        blob.content_type = content_type

        blob.upload_from_file(image.file)
        url = blob.public_url
        # If the public URL is not available, construct it manually
        if not url:
            # f'https://storage.googleapis.com/{bucket.name}/images/{image.name}'
            url = 'no public url'

        return url

    def get_all_image_urls(self):
        return 'ji'


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
    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params["id"]
            if id is not None:
                stu = User.objects.get(id=id)
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
