# debug_settings.py
#
# To run this project in debug mode, launch it using
#     python manage.py runserver --settings=debug_settings 0.0.0.0:8000
# instead of
#     python manage.py runserver 0.0.0.0:8000
#

# Start by pulling in the normal settings
from googlebackup.settings import *

# force debug mode
DEBUG = True
import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)