from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, LikeDislike, Profile
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm
import json


def index(request):
    return render(request, 'index.html')  # This loads your HTML file

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('feed')  # Redirect to homepage after signup
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm()  # Initialize form first

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")  # Redirect after successful login

    return render(request, "login.html", {"form": form})

def landing(request):
    return render(request, "landing.html")  # Use a template inside the users app


@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        # Handling new post creation
        if 'content' in request.POST or 'image' in request.FILES:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()

                # If AJAX request, return only the new post
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return render(request, 'single_post.html', {'post': post})

                return redirect("feed")

        # Handling new comment submission (AJAX)
        elif 'text' in request.POST and 'post_id' in request.POST:
            post_id = request.POST.get('post_id')
            text = request.POST.get('text')
            post = Post.objects.get(id=post_id)

            comment = Comment.objects.create(user=request.user, post=post, text=text)

            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'text': text,
                'comment_count': post.comments.count()
            })

    else:
        form = PostForm()

    return render(request, 'feed.html', {'form': form, 'posts': posts})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Fetch the post by ID
    return render(request, 'post_detail.html', {'post': post})


def custom_csrf_failure_view(request, reason=""):
    return redirect('/feed/')  # Redirect to feed page on CSRF failure




@login_required
def like_dislike_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, post=post)

    if action == "like":
        like_dislike.like = True
        like_dislike.dislike = False
    elif action == "dislike":
        like_dislike.like = False
        like_dislike.dislike = True

    like_dislike.save()

    # Count total likes and dislikes
    likes_count = LikeDislike.objects.filter(post=post, like=True).count()
    dislikes_count = LikeDislike.objects.filter(post=post, dislike=True).count()

    return JsonResponse({"success": True, "likes": likes_count, "dislikes": dislikes_count})



@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Load JSON data
            text = data.get("text", "").strip()  # Ensure text is not None

            if not text:
                return JsonResponse({"success": False, "error": "Comment cannot be empty!"}, status=400)

            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=request.user, text=text)

            return JsonResponse({
                "success": True,
                "username": request.user.username,
                "text": comment.text
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # Try to fetch the profile, if not found, create one
    profile, created = Profile.objects.get_or_create(user=profile_user)
    
    posts = Post.objects.filter(user=profile_user)
     # ✅ Get the logged-in user's following list
    following = request.user.profile.following.all()
    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "following": following
    }
    return render(request, "profile.html", context)





from django.shortcuts import render
from django.utils.timezone import now, timedelta
from django.core.cache import cache
from django.db.models import Count
from .models import Post

def trending_posts_view(request):
    # Check if cached trending posts exist
    trending_posts = cache.get('trending_posts')

    if not trending_posts:
        # Fetch posts sorted by like count dynamically
        trending_posts = Post.objects.annotate(like_count=Count('likes_dislikes')).order_by('-like_count')[:10]

        # Cache the trending posts for 24 hours
        cache.set('trending_posts', list(trending_posts), timeout=86400)  # 24 hours

    return render(request, 'trending.html', {'trending_posts': trending_posts})





@login_required
def follow_unfollow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = get_object_or_404(Profile, user=user_to_follow)
    current_user_profile = get_object_or_404(Profile, user=request.user)
    is_following = request.user in profile_to_follow.followers.all()  # ✅ Check if user is following
    
    
    if profile_to_follow != current_user_profile:
        if request.user in profile_to_follow.followers.all():
            profile_to_follow.followers.remove(request.user)
            current_user_profile.following.remove(user_to_follow)  # Remove from following
        else:
            profile_to_follow.followers.add(request.user)
            current_user_profile.following.add(user_to_follow)  # Add to following

    # Count updates
    followers_count = profile_to_follow.followers.count()
    following_count = current_user_profile.following.count()

    return JsonResponse({
        "following": request.user in profile_to_follow.followers.all(),
        "followers_count": followers_count,
        "following_count": following_count
    })


from .forms import ProfileUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)

    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign logged-in user
            post.save()
            return redirect('feed')  # Redirect to feed after post creation
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


API_KEY = ""

import requests
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings


# Render the AI Page
def ai_page(request):
    return render(request, "ai.html")

# Generate AI Art from User Prompt
def generate_image(request):
    if request.method == "GET":
        prompt = request.GET.get("prompt", "").strip()

        if not prompt:
            return JsonResponse({"error": "Prompt is required!"}, status=400)

        # 🖌️ Improve Prompt for AI & Artists
        improved_prompt = f"A high-quality, artistic, step-by-step creation of {prompt}, beginner-friendly, simple strokes, easy to recreate, digital painting, concept art."

        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "dall-e-3",  # 🎨 Using DALL-E 3 for better results
            "prompt": improved_prompt,
            "n": 1,
            "size": "1024x1024"
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            ai_response = response.json()
            image_url = ai_response["data"][0]["url"]

            # 🖌️ Generate Step-by-Step Guide for Artists
            guide = generate_art_steps(prompt)

            return JsonResponse({
                "image_url": image_url,
                "art_guide": guide
            })
        else:
            return JsonResponse({"error": f"Failed to generate image. API Response: {response.text}"}, status=400)

# ✅ Function to Create an Artist-Friendly Guide
def generate_art_steps(subject):
    return [
        f"1️⃣ Sketch: Start with a light pencil sketch of {subject}. Focus on proportions.",
        f"2️⃣ Outline: Use a fine pen or brush to define the shape clearly.",
        f"3️⃣ Base Colors: Apply the main colors lightly with a brush or digital tool.",
        f"4️⃣ Shading & Highlights: Add shadows and light to give depth.",
        f"5️⃣ Final Touches: Enhance details and refine edges for a polished look."
    ]