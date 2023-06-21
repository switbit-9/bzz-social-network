from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import User, Profile



#Mix Profile info with User info
class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)