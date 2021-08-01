
from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.compose_post, name="compose_post"),
    
     # API Routes
    path("getsection/<str:section>", views.get_posts, name="getsection"),
    path("getuser/<int:id>", views.getuser, name="getuser"),
    path("followuser", views.followuser, name="followuser"),

  



 


]   
 