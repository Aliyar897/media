# mainpageapp/management/commands/run_test_task.py

from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates a periodic task to run test_celery every 2 seconds.'

    def handle(self, *args, **options):
        # Create an interval schedule for every 2 seconds
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=2,
            period=IntervalSchedule.SECONDS,
        )

        # Create a periodic task
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Run Test Celery Task',
            task='mainpageapp.tasks.test_celery',  # Path to your task
        )

        self.stdout.write(self.style.SUCCESS('Periodic task created successfully.'))
