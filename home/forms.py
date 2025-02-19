from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django import forms
from .models import Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'name': 'title', 'id': 'title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'name': 'description', 'id': 'description', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'name': 'price', 'id': 'price', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'name': 'image', 'id': 'image', 'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
