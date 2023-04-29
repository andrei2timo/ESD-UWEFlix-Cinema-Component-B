"""
WSGI config for web_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""
# The wsgi.py file is used to configure the web server gateway interface (WSGI) for a Django project. 
# It sets up the Django application to be run in a production server environment. This file imports the 
# get_wsgi_application() function from Django's core wsgi module and calls it to create the WSGI application 
# object named "application". This WSGI application object is used by the web server to interface with 
# the Django application. The os.environ statement sets the DJANGO_SETTINGS_MODULE environment variable 
# to the name of the project's settings module. The comments in the file provide more information on 
# how to use this file in a deployment scenario.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

application = get_wsgi_application()
