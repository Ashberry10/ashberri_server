from rest_framework import serializers
from .models import FriendShip

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        # receiver_user_id = serializers.IntegerField()
        fields = ['sender']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        # receiver_user_id = serializers.IntegerField()
        fields = ['id','status','created_at','sender']
        # friend_status = serializers.CharField(max_length=100)


class FriendShipStatusSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField()
    friend_status = serializers.CharField(max_length=100)