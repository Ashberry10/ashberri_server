from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        # receiver_user_id = serializers.IntegerField()
        fields = '__all__'