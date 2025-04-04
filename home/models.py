# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    profile_picture = models.ImageField(upload_to='profile_pics/', default='static/default.jpg')
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)  # Add this field!
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.user.username} Profile"

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize the profile picture
        if self.profile_picture:
            img_path = self.profile_picture.path
            img = Image.open(img_path)

            # Resize if image is too large
            max_size = (300, 300)
            img.thumbnail(max_size)
            img.save(img_path)
    def __str__(self):
        return f"{self.user.username} Profile"

    def is_followed_by(self, user):
        """Check if a user follows this profile"""
        return self.followers.filter(id=user.id).exists()



# Function to validate image size (max 5MB)
def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB limit
    if image.size > max_size:
        raise ValidationError("Image file too large (Max 5MB)")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the post
    image = models.ImageField(upload_to='posts/', validators=[validate_image_size], blank=True, null=True)  # Image validation added
    caption = models.TextField(blank=True)  # Optional caption
    created_at = models.DateTimeField(auto_now_add=True)  # Stores post creation time
    image = models.ImageField(upload_to='post/',default='default_post.jpg')  # Image Field
    title = models.CharField(max_length=255,default="Untitled post")  # Artwork Title
    description = models.TextField(default="No description provided.")  # Detailed Description
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # Price Field
    category = models.CharField(max_length=100,default="General", choices=[
        ('painting', 'Painting'),
        ('sculpture', 'Sculpture'),
        ('digital', 'Digital Art'),
        ('other', 'Other')
    ])  # Art Category
    availability = models.BooleanField(default=True)  # True if available, False if sold

    def __str__(self):
        return self.title

    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"  # Display first 20 chars of caption
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the post first

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Resize image to a square format (Instagram-like)
            max_size = (1080, 1080)  # Instagram max resolution
            img.thumbnail(max_size)
            img.save(img_path)  # Save resized image
    def total_likes(self):
        return LikeDislike.objects.filter(post=self, like=True).count()

    def total_dislikes(self):
        return LikeDislike.objects.filter(post=self, dislike=True).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class LikeDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes_dislikes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')  # Prevents multiple reactions from the same user
        
class Order(models.Model):
    # Your fields here
    x=5
    
    
class HomeChatroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Chatroom(models.Model):
    name = models.CharField(max_length=5000)
    
    def _str_(self):
        return self.name

class Chat(models.Model):
    chat_content = models.CharField(max_length=5000)
    user = models.CharField(max_length=5000)
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    


