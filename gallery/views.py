from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArtworkForm, ProfileForm, RegisterForm
from .models import Artwork, Profile


def home(request):
    artworks = Artwork.objects.select_related('author', 'category')
    return render(request, 'gallery/home.html', {'artworks': artworks})


def artwork_detail(request, artwork_id):

    artwork = get_object_or_404(
        Artwork.objects.select_related('author', 'category'),
        id=artwork_id,
    )

    return render(request, 'gallery/artwork_detail.html', {'artwork': artwork})


@login_required
def create_artwork(request):

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.author = request.user
            artwork.save()
            messages.success(request, 'Работа опубликована.')
            return redirect('artwork_detail', artwork_id=artwork.id)
    else:
        form = ArtworkForm()

    return render(request, 'gallery/artwork_form.html', {'form': form})


def profile_detail(request, username):

    profile_user = get_object_or_404(User, username=username)
    artist_profile, _ = Profile.objects.get_or_create(
        user=profile_user,
        defaults={'display_name': profile_user.username},
    )
    artworks = profile_user.artworks.select_related('category')

    return render(
        request,
        'gallery/profile_detail.html',
        {
            'profile_user': profile_user,
            'artist_profile': artist_profile,
            'artworks': artworks,
        },
    )


@login_required
def dashboard(request):

    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'display_name': request.user.username},
    )

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    artworks = request.user.artworks.select_related('category')
    return render(request, 'gallery/dashboard.html', {'form': form, 'artworks': artworks})


def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
