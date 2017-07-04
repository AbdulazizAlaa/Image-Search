# from app import settings
# from django.core.management import setup_environ
# # setup_environ(settings)
# os.environ("DJANGO_SETTINGS_MODULE") = app.settings

# from django.conf import settings
# from contentui import settings
# settings.configure(settings)

# import sys, os
# sys.path.append('/home/nada/GradProj/Image-Search/app/')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
# from django.conf import settings

from django_seed import Seed

from django.contrib.auth.models import User
from image.models import Image, Tag

seeder = Seed.seeder()

seeder.add_entity(Image, 15)
seeder.add_entity(User, 15)
seeder.add_entity(Tag, 15)
seeder.execute()
