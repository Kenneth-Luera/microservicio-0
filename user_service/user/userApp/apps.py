from django.apps import AppConfig


class UserappConfig(AppConfig):
    name = 'user.userApp'

    def ready(self):
        import user.userApp.signals
