from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LikedPost, User, Post, Profile, Follow
# Register your models here.


admin.site.register(User, UserAdmin) 

@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'body', 'created', 'active')


@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id',  'user', 'following', 'follower',  'exist')


@admin.register(Follow) 
class FollowAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_from', 'user_to', 'is_following')
 
@admin.register(LikedPost) 
class LikedPostAdmin(admin.ModelAdmin):
  list_display = ('id', 'liker', 'post', 'liked')
 