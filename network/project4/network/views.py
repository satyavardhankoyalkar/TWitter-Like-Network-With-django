from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Handle Like removal
@login_required
def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "Like removed!"})


# Handle Like addition
@login_required
def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    new_like = Like(user=user, post=post)
    new_like.save()
    return JsonResponse({"message": "Like added!"})


# Toggle like functionality
@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return JsonResponse({"liked": False})
        return JsonResponse({"liked": True})
    return JsonResponse({"error": "Invalid request method."}, status=405)


# View all posts with pagination and like tracking
def all_posts_view(request):
    posts = Post.objects.all()
    who_you_liked = Like.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    return render(request, "network/all_posts.html", {
        "posts_of_the_page": posts,
        "whoYouLiked": list(who_you_liked),
    })


# Edit post functionality
@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.user:
            try:
                data = json.loads(request.body)
                post.content = data.get("content", "").strip()
                post.save()
                return JsonResponse({"data": post.content})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return HttpResponseForbidden("You are not authorized to edit this post.")
    return JsonResponse({"error": "Invalid request method."}, status=405)


# Index view with pagination and like count
def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    # Track likes for each post
    all_likes = Like.objects.all()
    who_you_liked = []
    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                who_you_liked.append(like.post.id)
    except:
        who_you_liked = []

    return render(request, "network/index.html", {
        "allPosts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "whoYouLiked": who_you_liked
    })


# Create new post
@login_required
def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))


# View a user's profile with their posts
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    # Check follow status
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)
    is_following = False
    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
    except:
        is_following = False

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "allPosts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "isFollowing": is_following,
        "user_profile": user
    })


# View posts from users the current user is following
def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_people = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()
    following_posts = [post for post in all_posts if post.user in [person.user_follower for person in following_people]]

    # Pagination
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page
    })


# Follow a user
def follow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow(user=current_user, user_follower=user_follow_data)
    f.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


# Unfollow a user
def unfollow(request):
    user_follow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    f = Follow.objects.get(user=current_user, user_follower=user_follow_data)
    f.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


# Login view
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


# Logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register view
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
