from django.conf import settings

# Site debug
DETECTIVE_DEBUG = getattr(settings, 'DEBUG', False)

# If True, internal server error responses with exception (500) are stored in database
DETECTIVE_SAVE_ERROR_RESPONSES = getattr(settings, 'DETECTIVE_SAVE_ERROR_RESPONSES', True)

# Should Ajax requests be tracked?
DETECTIVE_TRACK_AJAX_REQUESTS = getattr(settings, 'DETECTIVE_TRACK_AJAX_REQUESTS', True)

# Should anonymous requests be tracked?
DETECTIVE_TRACK_ANONYMOUS_REQUESTS = getattr(settings, 'DETECTIVE_TRACK_ANONYMOUS_REQUESTS', True)
