from django.apps import AppConfig

# This code defines an `AppConfig` class for the `uweflix` Django application. It sets the default auto 
# field to a `BigAutoField` and sets the name of the app to `uweflix`. This configuration can be used to 
# customize the behavior of the app when it is loaded by Django.
class UWEFlixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uweflix'
