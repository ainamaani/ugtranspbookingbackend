from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import ResetCode


class Command(BaseCommand):
    help = 'Deletes reset codes older than five minutes'

    def handle(self, *args, **options):
        five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
        old_reset_codes = ResetCode.objects.filter(created_at__lt=five_minutes_ago)
        old_reset_codes.delete()