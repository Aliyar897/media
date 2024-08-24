from django.apps import AppConfig


class MainpageappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpageapp'

    def ready(self):
        # Import the ai_model module to ensure it is loaded when the app starts
        from . import ai_model