import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebPyRobot.settings")

django.setup()
import backend.multiclientServer
