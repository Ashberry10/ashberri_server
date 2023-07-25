






from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.exceptions import ValidationError

from account.models import User


class UserModelAdmin(BaseUserAdmin):
  

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'name', 'is_admin','day', 'month', 'year','file','gender',)
    # list_display = ('id','email', 'name','tc','Dfirst','Cfirst', 'is_admin','date_of_birth')

    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
 
        ('Personal info', {'fields': ('name','day','month','year','gender',)}),
        # ('Personal info', {'fields': ('name','tc','Dfirst','Cfirst','date_of_birth')}),


        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
              'fields': ('email', 'name','gender',),
            # 'fields': ('email', 'name','file','day', 'month', 'year','password',),
            # 'fields': ('email', 'name','tc','date_of_birth','Cfirst','Dfirst', 'password1', 'password2'),
# 
        }),
    )
    search_fields = ('email','D_second','C_second','password')
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)