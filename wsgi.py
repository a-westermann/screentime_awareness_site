import os
from django.core.wsgi import get_wsgi_application

# Ensure you set this to your settings module, e.g., 'myproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screentime_awareness_site.settings.py')

application = get_wsgi_application()
