from rest_framework import serializers
from .models import FriendShip

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        # receiver_user_id = serializers.IntegerField()
        fields = ['receiver']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        # receiver_user_id = serializers.IntegerField()
        fields = ['id','status','created_at','sender']



