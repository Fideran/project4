
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('user', views.userProfile, name="user"),
    path('profile/<int:profile_id>', views.profile, name="profile"), 
    path('allposts/<str:load_post>/<int:page_num>', views.loadPost, name='posts'),#Add pagination ('allposts/<str:load_post>/<int:page_num>)
    path('new_post', views.newPost, name="new_post"),
    path('edit_post', views.editPost, name="edit_post"), 
    path('like', views.like, name="like"),
    path('unlike', views.unlike, name="unlike"),
    path('follow', views.follow, name="follow"),
    path('unfollow', views.unfollow, name="unfollow"),
    path('profile/follower', views.follower_num, name="follower")
]
