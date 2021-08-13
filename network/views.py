import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import fields
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import tree 

from .models import Profile, User, Post, Follow


from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
#from common.decorators import ajax_required


class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'rows':1})
        }
        labels = {
            'body': 'New Post', 
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



@login_required
def compose_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)  
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            
            new_post.poster = request.user          
            new_post.save()       
       
            if new_post.poster.is_authenticated:
                obj, created = Profile.objects.get_or_create(
                    username=request.user,                    
                    defaults={'exist':True}
                    )  
                  
    else:
        post_form: PostForm() 
    return HttpResponseRedirect(reverse ('index'))
    #return render(request, "network/index.html",)


   
    # Returns the entire API. But am unable to reach the keys and its values at the moment
    """
    def get_posts(request, section):
        allposts = list(Post.objects.values())
        return JsonResponse(allposts, safe=False)
    """


def get_posts(request, section):
    if section == "allposts":
        posts = Post.objects.filter(active=True)
        return JsonResponse([post.serialize() for post in posts], safe=False)
   
    else:
        #posts = posts.order_by("-created").all()
        return JsonResponse({"error":"No post yet"}, status=404)
  
 

@login_required
def getuser(request, id):       

    # Query for requested user profile and its posts
    try:      
        post_id = get_object_or_404(Post, id=id)
        posts = Post.objects.filter(poster=post_id.poster, active=True).all() 
        user = Profile.objects.filter(username=post_id.poster, exist=True)
        currentUser = Profile.objects.filter(username=request.user) 
        userdata = [*user, *posts, *currentUser ]
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return requested user profile and its posts
    if request.method == "GET":
        return JsonResponse([user.serialize() for user in userdata], safe=False)

#@ajax_required
#@csrf_exempt
#require_POST
def followuser(request):

    if request.method == "POST":
        #return JsonResponse({"error": "User not found."}, status=404)
        
        action = request.POST["action"]
        user_followed = request.POST["followed"]
        #user_follower = request.POST["follower"]
        
        
        
        if user_followed:            

                #followed = Profile.objects.get(username=user_followed)

                followed = User.objects.get(username=user_followed)
                if action:
                    
                    #followed.user_follows.create(request.user)
                    
                    
                    p = Follow.objects.create(user_from=request.user, user_to=followed)
                    p.save()
                
                    return JsonResponse({"status":"ok"})
        
            #return JsonResponse({"status": "error"})

    return JsonResponse({"status": "error"})

    
    


def index(request):
    return render(request, "network/index.html", {
            "form": PostForm(),
        })


def login_view(request):
    if request.method == "POST": 

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)



        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
