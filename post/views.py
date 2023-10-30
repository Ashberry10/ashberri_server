from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics

from account.serializers import UpdateUserSeriailzer
from post.models import Comment, Like, Post, Share
from post.serializers import CommentSerializer, GetCommentSerializer, LikeSerializer, PostByIdSerializer, PostSerializer, ShareSerializer


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        luser = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=luser)
            data = serializer.data
            ResponseBody = {
                "success": True,
                "message": "Post created successfully",
                "data": data
            }
            return Response(ResponseBody, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id)
        serializer = PostByIdSerializer(post,many=True)
        data = serializer.data
        like = Like.objects.filter(post_id =1)
        like_data = LikeSerializer(like, many=True)
        ResponseBody = {
            "success": True,
            "message": "Post fetched successfully",
            "data": data,
            "like": like_data.data
        }
        return Response(ResponseBody)  # todo add more details in resposne

    def patch(self, request, post_id):  # update user profile
        user = post_id  # user refer to the loged in user (token)
        serializer = UpdateUserSeriailzer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            # serializer.save()
            return Response("UPDATED work in progress")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

class GetPostByUserID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):

        post_data = Post.objects.filter(user_id = user_id)
        user_post_data = PostSerializer(post_data, many=True)

        ResponseBody = {
            "success": True,
            "message": "Post fetched successfully",
            "data": user_post_data.data
        }
        return Response(ResponseBody)


class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            user = request.user

            existing_like = Like.objects.filter(user=user, post=post).first()
            
            if existing_like:
                existing_like.delete()
                message = "Post unliked successfully"
                status_code = status.HTTP_200_OK
            else:
                like = Like(user=user, post=post)
                like.save()
                message = "Post liked successfully"
                status_code = status.HTTP_201_CREATED
            
            response_data = {"message": message}
            return Response(response_data, status=status_code)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        # post = Post.objects.filter(id=post_id)

        like = Like(user=request.user, post=post)

        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)  # todo add more details in resposne

class ListLikesForPost(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)


class CountLikesForPost(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        like_count = Like.objects.filter(post_id=post_id).count()
        return Response({'like_count': like_count})

class SharePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        share = Share(user=request.user, post=post)
        share.save()
        return Response(status=status.HTTP_201_CREATED)

class Comments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentByID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, comment_id):
        comments = Comment.objects.filter(id=comment_id)
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data)


    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({'message': 'comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'error': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CommentByPostID(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user, post_id=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = GetCommentSerializer(comments, many=True)
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
