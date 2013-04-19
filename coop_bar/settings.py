from django.conf import settings as django_settings

DISPLAY_MESSAGES_LOG = getattr(django_settings, 'DISPLAY_MESSAGES_LOG', False)
