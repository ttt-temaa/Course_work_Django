from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser


class Command(BaseCommand):
    help = "Создание группы 'Менеджеры' с правами на просмотр и редактирование пользователей"

    def handle(self, *args, **options):
        group_name = "Менеджеры"
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' успешно создана."))
        else:
            self.stdout.write(self.style.WARNING(f"Группа '{group_name}' уже существует."))

        content_type = ContentType.objects.get_for_model(CustomUser)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "view_customuser",
                "change_customuser",
            ]
        )
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(f"Добавлены права на пользователей: {[p.codename for p in permissions]}"))
