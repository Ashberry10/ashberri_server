from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import datetime
import json
from django.contrib.auth.models import User
# Create your models here.



#Custon User Manager
# args = ap.parse_args()
class UserManager(BaseUserManager):
    # def create_user(self, email,name,tc, Dfirst,Cfirst,date_of_birth,password=None,password2=None):
    def create_user(self, email,name,day,month,year,profile_photo,password=None):
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
            # D_second=D_second,
            # C_second=C_second,
            # C_first=C_first,
            # D_first=D_first,
            name=name,
            profile_photo=profile_photo
            # date_of_birth=date_of_birth,
            # tc = tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self, email, name,password=None):
        """
        Creates and saves a User with the given email,name,tc 
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            name= name,
            
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
    # tc = models.BooleanField()
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
    profile_photo = models.ImageField(upload_to='profile_photo/%Y/%m/%d',max_length=255,null=True,blank=True)
    # date_of_birth = models.DateField(attrs={'input_formats'=['%d-%m-%Y']} )   
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

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


