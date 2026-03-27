"""
Django command to create a superuser if it doesn't already exist.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from decouple import config


class Command(BaseCommand):
    """Create a superuser if it doesn't exist."""

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=config('SUPERUSER_USERNAME'),
            help='Superuser username'
        )
        parser.add_argument(
            '--email',
            type=str,
            default=config('SUPERUSER_EMAIL'),
            help='Superuser email'
        )
        parser.add_argument(
            '--password',
            type=str,
            default=config('SUPERUSER_PASSWORD'),
            help='Superuser password'
        )

    def handle(self, *args, **options):
        """Entry point for command."""
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'✓ Superuser "{username}" already exists. Skipping creation.')
            )
        else:
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Superuser "{username}" created successfully!')
            )
