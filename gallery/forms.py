from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Artwork, Profile


class RegisterForm(UserCreationForm):
    """Форма регистрации на основе стандартной формы Django."""

    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ArtworkForm(forms.ModelForm):
    """Форма публикации новой работы."""

    class Meta:
        model = Artwork
        fields = ('title', 'image', 'description', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProfileForm(forms.ModelForm):
    """Форма редактирования личного кабинета."""

    class Meta:
        model = Profile
        fields = ('display_name', 'bio', 'avatar', 'location')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
