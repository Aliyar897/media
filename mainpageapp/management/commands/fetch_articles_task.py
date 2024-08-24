# mainpageapp/management/commands/fetch_articles_task.py

from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates a periodic task to fetch articles every hour.'

    def handle(self, *args, **options):
        # Create an interval schedule for every hour
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        # Create a periodic task
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Fetch Articles Task',
            task='mainpageapp.tasks.fetch_articles',  # Path to your task
        )

        self.stdout.write(self.style.SUCCESS('Periodic task created successfully.'))
