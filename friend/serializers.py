from rest_framework import serializers
from .models import FriendShip

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        # receiver_user_id = serializers.IntegerField()
        fields = '__all__'