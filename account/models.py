

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import datetime
import json
from django.contrib.auth.models import User
# Create your models here.
from django.dispatch import receiver
from friend.models import FriendList
from django.db.models.signals import post_save

#Custon User Manager
# args = ap.parse_args()
class UserManager(BaseUserManager):
    # def create_user(self, email,name,tc, Dfirst,Cfirst,date_of_birth,password=None,password2=None):
    def create_user(self, email,name,day,month,year,gender,password=None):
    # def create_user(self, email,name,date_of_birth,password=None):


        """
        Creates and saves a User with the given email,name,tc 
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
            day=day,
            month=month,
            year=year,
            gender= gender,
            # D_second=D_second,
            # C_second=C_second,
            # C_first=C_first,
            # D_first=D_first,
            name=name,
            # file=file
            # date_of_birth=date_of_birth,
            # tc = tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self, email, name,day,month,year,file,password=None):
        """
        Creates and saves a User with the given email,name,tc 
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            name= name,
            day=day,
            month=month,
            year=year,
            file=file
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    
 
    name= models.CharField(max_length=200)
 
    # D_first= models.IntegerField(default=0)
    # C_first= models.IntegerField(default=0)
    C_second = models.IntegerField(default=0)
    D_second = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    # compatibility = models.IntegerField(default=0)
    # date_of_birth = models.DateField(null=True)
    date_of_birth = models.DateTimeField(default=0)
    file = models.ImageField(upload_to='profile_photo/%Y/%m/%d',null=True,blank=True,verbose_name='profile_photo',default='defaultuserpic.png')
    # date_of_birth = models.DateField(attrs={'input_formats'=['%d-%m-%Y']} )   
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    gender = models.CharField(max_length=10, choices=[('male', 'male'), ('female', 'female'),('other', 'other')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']






    def __str__(self):
        return self.email
    @property
    def C_second(self):
    #    dob = self.date_of_birth

       day = self.day
         
       month = self.month
       year = self.year

       dobsum = day + year + month

       def digSum(totaldob):     
          if (totaldob == 0):
           return 0
          if (totaldob % 9 == 0):
            return 9
          else:
             return (totaldob % 9)

       C_second = digSum(dobsum)
      

       return C_second

    @property
    def D_second(self):
    #    dob = self.date_of_birth
       day = self.day
       def digSum(totaldob):     
          if (totaldob == 0):
           return 0
          if (totaldob % 9 == 0):
            return 9
          else:
             return (totaldob % 9)

       D_second = digSum(day)
      

       return D_second








    @property
    def date_of_birth(self):
       day = self.day
         
       month = self.month
       year = self.year



    #    date_of_birth  = {month},'/',{year}

       date_of_birth = datetime.date(year,month,day)

       json_str = json.dumps(date_of_birth,default=str)
    #    print (type(json_str))
       json_object = json.loads(json_str)

       print(json_object)
       
    #    my_new_string  = json_str.replace("\","3")
       return json_object




    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
@receiver(post_save, sender=User)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)

#User Post Model
class UserPost(models.Model):
   url = models.URLField()
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.url

# #models to review
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)
#     profile_picture = models.ImageField(upload_to='profile_pictures')
#     registration_date = models.DateTimeField(auto_now_add=True)

# class Post(models.Model):
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

# class Comment(models.Model):
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

# class Friendship(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE)

# class Notification(models.Model):
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')