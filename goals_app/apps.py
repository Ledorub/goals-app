from django.apps import AppConfig


class GoalsAppConfig(AppConfig):
    name = 'goals_app'

    def ready(self):
        import goals_app.signal_handlers
