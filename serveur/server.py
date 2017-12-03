import os
import django

#Configuration de django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebPyRobot.settings")

django.setup()

#Lancement du serveur
from backend.RobotsServer import run
run()
