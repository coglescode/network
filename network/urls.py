
from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.compose_post, name="compose_post"),
    path("editpost", views.editpost, name="editpost"),
    path("getuser/<str:username>", views.getuser, name="getuser"),
    path("followed", views.followed_posts_list, name="followed"),  
    path("followuser", views.followuser, name="followuser"),
    path("savecounter", views.savecounter, name="savecounter"),
    path("likepost", views.likepost, name="likepost"),

]   
 