from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User, Profile
# Register your models here. 


admin.site.register(User, UserAdmin) 


@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id',  'username',  'exist')



@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'poster', 'body', 'created', 'updated', 'active')


