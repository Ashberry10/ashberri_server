from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here......
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
        remover_friends_list = self #person terminating the FriendShip

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

class FriendShip(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
            return f'{self.sender.name} -> {self.receiver.name}'


    def accept(self):
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()
   






    def reject(self):
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()

