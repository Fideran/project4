import json
from json.decoder import JSONDecodeError
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Follow, Followed, Follower, Like, Post, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    posts = Post.objects.all()
    objects = [post.serialize_json() for post in posts]
    p = Paginator(objects, 10)
    return render(request, "network/index.html",{
        "pages": range(1,p.num_pages+1)
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
            follow = Follow(user = user)
            follow.save()
            follower = Follower(user = user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def userProfile(request):
    user = User.objects.get(username = request.user)
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

def loadPost(request, load_post, page_num):#eg: page_num = 1
    #PAGINATOR FOR ALL POSTS
    
    posts = Post.objects.all()
    posts = posts.order_by("-post_time").all()
    objects = [post.serialize_json() for post in posts]
    p = Paginator(objects, 10)
    if load_post == 'allposts' :#<======= 1
        posts = Post.objects.all()
        data = p.page(page_num).object_list
        #data = [post.serialize_json() for post in posts]
        return JsonResponse({"posts": data}, safe=False)
    elif load_post == 'following' :
        follower = Follower.objects.get(user = request.user)
        users = Followed.objects.filter(follower = follower )
        data2 = [user.serialize_json() for user in users]
        posts = Post.objects.all()
        posts= posts.order_by("-post_time").all()
        data = [post.serialize_json() for post in posts]
        return JsonResponse({"posts": data, 'follows': data2}, safe=False)
         
@csrf_exempt
@login_required
def like(request):
    if request.method != 'POST':
    #LIKES DISPLAY
        likes = Like.objects.all()
        likes = likes.order_by("-id").all()
        data = [like.serialize_json() for like in likes]
        return JsonResponse({"likes": data}, safe=False)
    #LIKES SAVE
    data = json.loads(request.body)
    user_id = data.get("user_id", "")
    post_id = data.get("post_id", "")
    user = User.objects.get(pk = user_id)
    post = Post.objects.get(pk = post_id)
    like = Like.objects.get(post = post)
    like.user.add(user)
    like.save()
    return JsonResponse({"Message": "Liked"})

@csrf_exempt
@login_required
def unlike(request):
    if request.method != 'POST':
        return JsonResponse({"Message":"Unlike is impossible"})

    data = json.loads(request.body)
    user_id = data.get("user_id", "")
    post_id = data.get("post_id", "")
    user = User.objects.get(pk = user_id)
    post = Post.objects.get(pk = post_id)
    unlike = Like.objects.get(post = post)
    unlike.user.remove(user)
    unlike.save()
    return JsonResponse({"Message": "Unliked"})

@csrf_exempt
@login_required
def newPost(request):
    if request.method != 'POST':
        return JsonResponse({"Error": "Impossible to create a new post"})

    data = json.loads(request.body)
    text_content = data.get("content", "")
    user_post = request.user
    like_number = 20
    comment_number = 26
    new_post = Post(
        user_post = user_post,
        text_content = text_content,
        like_number = 20,
        comment_number=26)
    new_post.save()
    like = Like(post=new_post)
    like.save()
    return render(request, "network/index.html", {
        "content": text_content
    })

@csrf_exempt
#@login_required
def editPost(request):
    if request.method != 'POST':
        return JsonResponse({"Error": "Impossible to edit your post"})
    data = json.loads(request.body)
    text_content = data.get("content", "")
    post_id = data.get("post_id", "")
    post_edit= Post.objects.get(pk=int(post_id))
    post_edit.text_content = text_content
    post_edit.save()

def profile(request, profile_id):
    user = User.objects.get(pk = int(profile_id))

    return JsonResponse(user.serialize())

@csrf_exempt
@login_required
def follow(request):
    if request.method != 'POST':
        #FOR FOLLOWED BUTTON DISPLAY
        all_followeds = Followed.objects.all()
        data = [follow_d.serialize_json() for follow_d in all_followeds]
        return JsonResponse({"followed":data}, safe=False)
    
    data = json.loads(request.body)
    followed_id = data.get("followed_id", "")
    follower = Follower.objects.get(user = request.user)

    fs = Followed.objects.all()
    for fd in fs:
        if fd.user.id == followed_id and fd.follower.user.id == request.user.id:
            return JsonResponse({"Message": "Unfollow"})
        
    followed = Followed(user = User.objects.get(pk=followed_id), follower = follower)
    followed.save()

    #FFILTER
    followed_filtered = Followed.objects.filter(user = User.objects.get(pk=followed_id))
    num = followed_filtered.count()
    #FOLLOWER NUMBER
    follower_num = Follow.objects.get(user = User.objects.get(pk=followed_id))
    follower_num.follower_num = num
    follower_num.save()

    all_followeds = Followed.objects.all()
    data = [follow_d.serialize_json() for follow_d in all_followeds]
    return JsonResponse({"Message": "Successfull Following"})


@csrf_exempt
@login_required
def unfollow(request):
    if request.method != 'POST':
        return JsonResponse({"Error": "Impossible to Unfollow"})

    data = json.loads(request.body)
    unfollowed_id = data.get("unfollowed_id", "")
    follower = Follower.objects.get(user = request.user)
    unfollowed = Followed.objects.get(user = User.objects.get(pk=unfollowed_id), follower = follower)
    unfollowed.delete()
    #FFILTER
    followed_filtered = Followed.objects.filter(user = User.objects.get(pk=unfollowed_id))
    num = followed_filtered.count()
    #FOLLOWER NUMBER
    follower_num = Follow.objects.get(user = User.objects.get(pk=unfollowed_id))
    follower_num.follower_num = num
    follower_num.save()
    return JsonResponse({"Message": "Successfull Unfollowing"})

def follower_num(request):
    followers = Follow.objects.all()
    data =[follower.serialize() for follower in followers]
    return JsonResponse({"Followers": data}, safe=False)


