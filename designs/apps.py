from django.apps import AppConfig


class DesignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designs'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals