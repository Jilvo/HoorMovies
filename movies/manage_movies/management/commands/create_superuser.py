from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser with specified username and password"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="superuser login")
        parser.add_argument("--password", required=True, help="superuser password")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"superuser « {username} » Already exists.")
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser « {username} » created."))
