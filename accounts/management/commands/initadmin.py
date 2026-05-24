import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создаёт суперпользователя, если он ещё не существует'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'   # сразу даём роль администратора
            )
            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь "{username}" создан')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Суперпользователь уже существует')
            )