from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_timeline_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    types = ContentType.objects.filter(app_label="timeline").values_list(
        "id", flat=True
    )
    grp, created = Group.objects.get_or_create(name="Timeline Manager")
    if created:
        permissions = Permission.objects.filter(content_type_id__in=types)
        grp.permissions.set(permissions)


class TimelineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "timeline"

    def ready(self):
        post_migrate.connect(create_timeline_group, sender=self)
