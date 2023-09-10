from rest_framework import serializers
from account.models import User
from post.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','password','D_second','gender','C_second','day','month','year'] 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content','image', 'timestamp']
