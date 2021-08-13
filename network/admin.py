from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User, Profile, Follow
# Register your models here. 


admin.site.register(User, UserAdmin) 


@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id',  'username', 'following', 'followers',  'exist')


@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'poster', 'body', 'created', 'updated', 'active')


@admin.register(Follow) 
class FollowAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_from', 'user_to', 'created')

