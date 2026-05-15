from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):


    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField('Имя на сайте', max_length=100, blank=True)
    bio = models.TextField('Описание', blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    location = models.CharField('Город/страна', max_length=120, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.display_name or self.user.username


class Artwork(models.Model):

    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='artworks/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance, display_name=instance.username)
