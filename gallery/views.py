from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArtworkForm, CommentForm, ProfileForm, RegisterForm
from .models import Artwork, Category, Comment, Like, Profile

SORT_OPTIONS = {
    'newest': '-created_at',
    'oldest': 'created_at',
    'title_asc': 'title',
    'title_desc': '-title',
    'popular': '-like_count',
}


def _artworks_queryset(user=None):
    qs = Artwork.objects.select_related('author', 'category').annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
    )
    if user and user.is_authenticated:
        qs = qs.annotate(
            user_liked=Exists(
                Like.objects.filter(artwork_id=OuterRef('pk'), user_id=user.id)
            )
        )
    return qs


def home(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'newest').strip()

    artworks = _artworks_queryset(request.user)

    if query:
        artworks = artworks.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(author__username__icontains=query)
        )

    if category_id.isdigit():
        artworks = artworks.filter(category_id=category_id)

    order = SORT_OPTIONS.get(sort, SORT_OPTIONS['newest'])
    artworks = artworks.order_by(order, '-id')

    return render(
        request,
        'gallery/home.html',
        {
            'artworks': artworks,
            'categories': Category.objects.all(),
            'query': query,
            'selected_category': category_id,
            'sort': sort if sort in SORT_OPTIONS else 'newest',
            'sort_options': SORT_OPTIONS,
        },
    )


def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(
        _artworks_queryset(request.user),
        id=artwork_id,
    )
    comments = (
        artwork.comments.select_related('user')
        .order_by('created_at')
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Войдите, чтобы оставить комментарий.')
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.artwork = artwork
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('artwork_detail', artwork_id=artwork.id)
    else:
        form = CommentForm()

    return render(
        request,
        'gallery/artwork_detail.html',
        {
            'artwork': artwork,
            'comments': comments,
            'comment_form': form,
        },
    )


@login_required
def toggle_like(request, artwork_id):
    if request.method != 'POST':
        return redirect('artwork_detail', artwork_id=artwork_id)

    artwork = get_object_or_404(Artwork, id=artwork_id)
    like, created = Like.objects.get_or_create(user=request.user, artwork=artwork)

    if not created:
        like.delete()
        messages.info(request, 'Лайк убран.')
    else:
        messages.success(request, 'Лайк поставлен.')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('artwork_detail', artwork_id=artwork_id)


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
    artworks = _artworks_queryset(request.user).filter(author=profile_user)

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

    artworks = _artworks_queryset(request.user).filter(author=request.user)
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
