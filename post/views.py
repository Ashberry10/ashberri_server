
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from account.serializers import UpdateUserSeriailzer
from post.models import Comment, Like, Post, Share
from post.serializers import CommentSerializer, LikeSerializer, PostSerializer, ShareSerializer


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
