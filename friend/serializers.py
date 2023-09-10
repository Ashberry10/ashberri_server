from rest_framework import serializers
from .models import FriendShip

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ['receiver','compatibility']

class AcceptOrRejectFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ['sender']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ['id','status','created_at','sender','compatibility']

class FriendShipStatusSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField()
    friend_status = serializers.CharField(max_length=100)
