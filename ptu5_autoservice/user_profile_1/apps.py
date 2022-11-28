from django.apps import AppConfig


class UserProfile1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile_1'

    def ready(self):
        from . signals import create_profile, save_profile