from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    
    pass




class Profile(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    user_folllows = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
    exist = models.BooleanField(default=True)
    

    def serialize(self):
        return {
            "id":self.id,
            "username": self.username.username,    
            "following": self.following,
            "followers": self.followers, 
            "exist": self.exist   
        }    
        
    def get_absolute_url(self):
        return reverse('getuser', args=[self.username])
        
    def __str__(self):
        return f'Profile for user {self.username}'
    



class Post(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)    
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "likes":self.likes,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "updated": self.updated.strftime("%b %d %Y, %I:%M %p"),
            "active": self.active           
        }

    def __str__(self):
        return f'Post {self.body} for user {self.poster.username}'

    class Meta:
        ordering = ('-created',)


"""
class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("User", on_delete=models.CASCADE )
   
   
    def serialize(self):
        return {
            "id": self.id,
            "post":self.post,
            "user": self.user.username,            
           
            #"unlikes":self.unlikes,            
            #"active": self.active           
        }
    
    def __str__(self):
        return f'Liked by {self.user}'


class Follows(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="following")
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    is_following = models.BooleanField(default=True)

    def serialize(self):
        return {
            "id":self.id,
            "user": self.user.username,    
            "following": self.following,
            "followers": self.followers, 
            "follows": self.follows   
        }
"""






    