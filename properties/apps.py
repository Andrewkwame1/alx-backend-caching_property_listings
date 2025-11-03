from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'
    
    def ready(self):
        # Import signal handlers to ensure they are registered
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Avoid raising on import errors during some management commands
            pass
