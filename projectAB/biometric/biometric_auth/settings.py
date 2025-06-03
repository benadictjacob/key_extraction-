import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ...existing code...
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# ...existing code...

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
# ...existing code...
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# ...existing code...
