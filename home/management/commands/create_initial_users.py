from django.core.management.base import BaseCommand

from home.models import User


INITIAL_USERS = [
    {
        "username": "tiago",
        "first_name": "Tiago",
        "last_name": "Lopes Carvalho",
        "role": User.Role.SYS,
        "password": "quiraing",
    },
    {
        "username": "sebas",
        "first_name": "Margarida",
        "last_name": "Sebastião",
        "role": User.Role.COLLAB,
        "password": "athensempraga",
    },
    {
        "username": "matilde",
        "first_name": "Matilde",
        "last_name": "Silva",
        "role": User.Role.COLLAB,
        "password": "athensempraga",
    },
    {
        "username": "caravana",
        "first_name": "Francisco",
        "last_name": "Caravana",
        "role": User.Role.COLLAB,
        "password": "athensempraga",
    },
    {
        "username": "carol",
        "first_name": "Carolina",
        "last_name": "João",
        "role": User.Role.COLLAB,
        "password": "athensempraga",
    },
    {
        "username": "tomas",
        "first_name": "Tomás",
        "last_name": "Ribeiro",
        "role": User.Role.COLLAB,
        "password": "athensempraga",
    },
]


class Command(BaseCommand):
    help = "Create initial project users (idempotent - skips existing usernames)"

    def handle(self, *args, **options):
        for raw in INITIAL_USERS:
            data = raw.copy()
            password = data.pop("password")
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults=data,
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Created user: {user.username} (role={user.role})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Skipped existing user: {user.username}")
                )
