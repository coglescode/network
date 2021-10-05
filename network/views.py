import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 

from .models import User, Post, Profile, Follow, LikedPost

from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'rows':'1', 'placeholder':'Speak your mind'})
        }
        labels = {
            'body': '', 
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form_div'



#Creates and save new posts
@login_required
def compose_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)  
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user          
            new_post.save()
    else:
        post_form: PostForm() 
    return HttpResponseRedirect(reverse ('index'))



#Edit posts view
@csrf_exempt 
@login_required
def editpost(request):
    if request.method != "POST":
        return JsonResponse({"error": "Most be method POST"})

    # Check posts
    data = json.loads(request.body)
    post = data.get("post", "")   
    postid = request.GET.get("id") 

    try:    
        posts = Post.objects.get(id=postid)
        if posts:
            Post.objects.filter(id=postid, user=request.user).update(body=post)      
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found"}, status=404)
    return JsonResponse({"message": "Post successfully updated."}, status=201)



#Save liked posts in a m2m in Post model
@require_POST
@csrf_exempt
@login_required
def likepost(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method POST   is required"}, status=400)
    
    data = json.loads(request.body)    
      
    post_id = data.get("post_id", "")
    action = data.get("action", "") 

    if post_id and action:           
        try:
            post = Post.objects.get(id=post_id)
            if action == "like":
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({"status":"ok"})          
        except:
            pass           
    return JsonResponse({"status":"error"})



@login_required
def getuser(request, username):  
    user = get_object_or_404(User, username=username)
    page_number = request.GET.get("page")

    try:
        posts = Post.objects.filter(user=user, active=True)
        userprofile = Profile.objects.filter(user=user, exist=True)        
        
        paginator = Paginator(posts, 10) # Show 10 posts per page 
        page_obj = paginator.get_page(page_number)  

    except Profile.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
    return render(request, "network/profile.html", {
        "profiles": userprofile,
        "posts": page_obj,
        "user": user,
        "page_number": page_number,
        "pages": page_obj.paginator.page_range       
    })



@csrf_exempt
@login_required
def followuser(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method GET is required"}, status=400)
    
    data = json.loads(request.body)    
 
    user = data.get("user", "")
    action = data.get("action", "") 

    if user and action:           
        try:
            user = User.objects.get(username=user)
            
            if action == "follow":
                Follow.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Follow.objects.filter(user_from=request.user, user_to=user).delete()                
            return JsonResponse({"status":"ok"})               
        except User.DoesNotExist:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})



#Save the counter for followings and followers
@csrf_exempt
@login_required
def savecounter(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method POST is required."}, status=400)

    data = json.loads(request.body)

    user = request.GET.get("user")
    follower_count = data.get("follower_count", "") 
    try: 
        user0 = get_object_or_404(User, username=request.user)
        total_following = user0.following.count()
        
        followed = User.objects.get(username=user)

        if user:             
            Profile.objects.filter(user=followed).update(follower=follower_count)

            Profile.objects.filter(user=request.user).update(following=total_following)
        else:
            Profile.objects.filter(user=followed, follower=follower_count).delete()

            Profile.objects.filter(user=request.user, following=total_following).delete()
            
    except Profile.DoesNotExist:
        return JsonResponse({"error":"Profile not found"})   
    return JsonResponse({"status":"ok"})   



#Brings followers posts to following page
@login_required
def followed_posts_list(request):
    
    followed_user = Follow.objects.filter(user_from=request.user).values_list("user_to")
    
    posts = Post.objects.filter(user__in=followed_user)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)        
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:        
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "network/following.html", {
        "posts": page_obj,         
        "page_number": page_number,   
        "pages": page_obj.paginator.page_range 
    })




def index(request):
    allposts = Post.objects.all()
    paginator = Paginator(allposts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": page_obj,         
        "pages": page_obj.paginator.page_range      
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

            rigestered = User.objects.get(username=username)
            perfil = Profile.objects.create(user=rigestered)
            perfil.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
