from django.db import models
from django.conf import settings


# Create your models here.
class FriendList(models.Model):

    user =  models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="friends")

    def __str__(self):
        return self.user.name

    def add_friend(self,account):
        """
        Add a new friend 
        """
        if  not account in self.friends.all():
            self.friends.add(account)
            self.save()


    def remove_friend(self,account):
        """
        Remove a friend 
        """
        if account in self.friends.all():
            self.friends.remove(account)
            

    def unfriend(self,removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_friends_list = self #person terminating the friendship

        #Remove Friend from remover friend list 
        remover_friends_list.remove_friend(removee)

        
        #Remove Friend from removee friend list 
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    
    def is_mutual_friend(self,friend):
        """
        Is this a friend?
        """  
        if friend in self.friends.all():
            return True
        return False



class FriendRequest(models.Model):
    """
    A Friend request consists of two main parts:
        1.SENDER:
            -Person sending/initiating the friend request 
        2. RECEIVER:
            -Person receiving the friend request 
    """

    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")

    is_active = models.BooleanField(blank=True,null=False,default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sender.name



    def accept(self):

        """
        Accept a friend request 
        Update both SENDER and REVEIVER friend lists 
        """
        receiver_friend_list  = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)

            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
            
    def decline(self):
        """
        Decline a friend request.
        Is it "declined" by setting the 'is_active' field to False
        """

        self.is_active =False
        self.save()



    def cancel(self):
        """
        Cancel a friend request 
        It is 'cancelled' by setting the 'is_active' field to False.
        This is only different with respect to "devlining" throgh the notification that is generated.
        """

        self.is_active = False 
        self.save()


        
        