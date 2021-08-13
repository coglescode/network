from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model



class User(AbstractUser):
    
    pass




class Follow(models.Model):
    user_from = models.ForeignKey( settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE, )
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created", )


class Profile(models.Model):
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    username = models.CharField(max_length=200, blank=True, )
    
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    #user_follows = models.ManyToManyField("self", through=Follow, related_name="following_users", symmetrical=False, blank=True)
    #user_follows = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="following_users", blank=True)
    
    exist = models.BooleanField(default=True)
    

    def serialize(self): 
        return {
            "id":self.id,
            "username": self.username,    
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
    created = models.DateTimeField(auto_now_add=True, db_index=True)
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


#Add following field to the User model dynamically
user_model = get_user_model()
user_model.add_to_class("following", models.ManyToManyField("self", through=Follow,
 related_name="following_users", symmetrical=False)
)


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






    