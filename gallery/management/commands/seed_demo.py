from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from gallery.models import Artwork, Category, Profile


class Command(BaseCommand):
    help = 'Creates demo categories, users and projects for a quick presentation.'

    def handle(self, *args, **options):
        categories = [
            Category.objects.get_or_create(name='Concept Art')[0],
            Category.objects.get_or_create(name='3D Environment')[0],
            Category.objects.get_or_create(name='Character Design')[0],
        ]

        demo_users = [
            ('alexart', 'Alex Art', 'Concept artist. Люблю фантастику и окружение.', 'Москва'),
            ('miradraws', 'Mira Draws', 'Рисую персонажей и игровые постеры.', 'Казань'),
        ]

        users = []
        for username, display_name, bio, location in demo_users:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('demo12345')
                user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.display_name = display_name
            profile.bio = bio
            profile.location = location
            profile.save()
            users.append(user)

        projects = [
            (
                'Neon Street Market',
                'Учебный концепт ночного рынка в киберпанк-городе. Здесь проверяю композицию, цвет и свет.',
                users[0],
                categories[0],
            ),
            (
                'Forest Gate',
                'Небольшая сцена окружения с воротами в лесу. Проект нужен для портфолио по environment art.',
                users[0],
                categories[1],
            ),
            (
                'Rogue Pilot',
                'Дизайн персонажа для sci-fi проекта: силуэт, костюм, основные цвета и характер.',
                users[1],
                categories[2],
            ),
        ]

        for title, description, author, category in projects:
            Artwork.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'author': author,
                    'category': category,
                },
            )

        self.stdout.write(self.style.SUCCESS('Demo projects created. Users password: demo12345'))
