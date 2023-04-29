"""
ASGI config for web_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
# `asgi.py` is the configuration file for ASGI (Asynchronous Server Gateway Interface) deployment for 
# the Django web project. It exposes an ASGI callable `application` as a module-level variable, which is 
# used to handle HTTP and WebSocket requests. The file sets the `DJANGO_SETTINGS_MODULE` environment 
# variable to the Django project's settings module (`web_project.settings`). For more information on 
# ASGI deployment, please refer to the Django documentation.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

application = get_asgi_application()
