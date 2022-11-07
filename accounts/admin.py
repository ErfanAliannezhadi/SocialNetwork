from django.contrib import admin
from .models import Follow, UserProfileModel
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = UserProfileModel


class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.register(Follow)
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
