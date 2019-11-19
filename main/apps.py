from django.apps import AppConfig


class SiteConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals
