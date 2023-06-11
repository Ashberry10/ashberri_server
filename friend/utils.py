from friend.models import FriendShip

def get_friend_request_or_false(sender,receiver):
    try:
        return FriendShip.object.get(sender=sender,receiver=receiver,isactive= True)
    except FriendShip.DoesNotExist:
        return False