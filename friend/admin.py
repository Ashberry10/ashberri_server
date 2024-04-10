from django.contrib import admin

# Register your models here.
from django.contrib import admin
from friend.models import FriendShip,FriendList

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

class Meta:
    model = FriendList

admin.site.register(FriendList,FriendListAdmin)

class FriendShipAdmin(admin.ModelAdmin):
    list_filter = ['sender','receiver']
    list_display = ['sender','receiver']
    search_fields = ['sender__username','sender__email','receiver__email','receiver__username']

    class Meta:
        model = FriendShip

admin.site.register(FriendShip,FriendShipAdmin)
