from ProductManagement.settings.base import *

SECRET_KEY = 'django-insecure-%+^q4t^a3$+w*&li^l3q_-)nv58(#j2#_rdc4bcdd7$0_*y)_m'

DEBUG = False

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['*']

print("\n" + "-" * 60)
print("Running server with production settings..")
print("-" * 60, "\n")
