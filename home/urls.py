from home import views
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.landing, name='landing'),  # Redirect after login
    path('feed/', views.feed, name='feed'),
    path("add_comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path('dislike/<int:post_id>/', views.like_dislike_post, {'action': 'dislike'}, name='dislike_post'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail_view'),
    path('reaction/<int:post_id>/<str:action>/', views.like_dislike_post, name='like_dislike_post'),
    path("create_post/", views.create_post, name="create_post"),
    ]