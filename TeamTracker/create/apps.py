from django.apps import AppConfig


class CreateConfig(AppConfig): # Configuration class for the create app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'create'
