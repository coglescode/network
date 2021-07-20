import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import fields
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 

from .models import Profile, User, Post

from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


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
        
    else:
        post_form: PostForm() 
    #return HttpResponseRedirect(reverse ('index'))
    return render(request, "network/index.html", {
        "form": PostForm()
    })


   
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

    # Query for requested email
    try:      
        post_id = get_object_or_404(Post, id=id)
        posts = Post.objects.filter(poster=post_id.poster, active=True).all()   
        user = Profile.objects.filter(username=post_id.poster, exist=True)

        x = [*user, *posts]
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse([user.serialize() for user in x], safe=False)
    






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
