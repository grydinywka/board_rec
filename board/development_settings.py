# -*- coding: utf-8 -*-

from .settings import *

DEBUG = True

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
DATABASES['default']['NAME'] = 'board_rec_db'


SOCIAL_AUTH_FACEBOOK_KEY = '1066975816723196'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e93ed95504aac968f493b9a9d6016550'