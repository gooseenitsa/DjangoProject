from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('artworks/new/', views.create_artwork, name='create_artwork'),
    path('artworks/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('artists/<str:username>/', views.profile_detail, name='profile_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
]
