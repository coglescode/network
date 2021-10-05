from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.contrib.auth import get_user_model


class User(AbstractUser):
    
    pass

class Follow(models.Model):   
    user_from = models.ForeignKey( settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE, )
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE, )
    is_following = models.BooleanField(default=True)
   
    
    def serialize(self):
        return {
            "user_from": self.user_from.username,
            "user_to": self.user_to.username,
            "is_following": self.is_following,            
            #"user": self.user.username,
            #"followers":self.followed
        }

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="profile")
    following = models.PositiveIntegerField(default=0)
    follower = models.PositiveIntegerField(default=0)
    exist = models.BooleanField(default=True)
    

    def serialize(self): 
        return {
            "id":self.id,
            "username": self.user.username,    
            "following": self.following,
            "follower": self.follower,             
            "exist": self.exist,              
        }    
        
    def get_absolute_url(self):
        return reverse('getuser', args=[self.user])
        
    def __str__(self):
        return f'Profile for user {self.user}'

    


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(null=False)  
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="posts_liked")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.user,
            "body": self.body,
            #"likes":self.likes,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            # "updated": self.updated.strftime("%b %d %Y, %I:%M %p"),
            "active": self.active           
        }

    def __str__(self):
        return f'Post {self.body} for user {self.user}'

    def get_absolute_url(self):
        return reverse('getuser', args=[self.user])

    class Meta:
        ordering = ('-created',)



class LikedPost(models.Model):  
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    post = models.IntegerField(blank=True)
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked = BooleanField(default=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.liker.username,
            "post": self.post,
            #"author": self.author,
            "liked": self.liked
        }

    def __str__(self):
        return f'Post {self.post} liked by {self.liker.username}'

    

#Add following field to the User model dynamically
user_model = get_user_model()
user_model.add_to_class("following", models.ManyToManyField("self", through=Follow,
 related_name="followers", symmetrical=False)
)






