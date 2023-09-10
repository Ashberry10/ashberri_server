from django.http import JsonResponse
from django.shortcuts import render
from account.models  import User
from post.models import Post
from .serializers import UserSerializer, PostSerializer

def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(content=query)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)
