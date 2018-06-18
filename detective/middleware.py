__author__ = 'Erik Telepovsky'

import sys

from django.db import utils

try:
    import psycopg2 as Database
    import psycopg2.extensions
except ImportError as e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)

DatabaseError = Database.DatabaseError

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object

from detective.models import TrackingLog
from detective.settings import DETECTIVE_TRACK_AJAX_REQUESTS, DETECTIVE_TRACK_ANONYMOUS_REQUESTS, \
    DETECTIVE_SAVE_ERROR_RESPONSES, DETECTIVE_DEBUG, DETECTIVE_SAVE_RESPONSES


class TrackingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Ajax request
        if request.is_ajax() and not DETECTIVE_TRACK_AJAX_REQUESTS:
            return response

        # Currently logged in user
        try:
            try:
                user = request.user if request.user.is_authenticated() else None
            except TypeError:
                user = request.user if request.user.is_authenticated else None
        except AttributeError:
            return response

        # Anonymous request
        if user is None and not DETECTIVE_TRACK_ANONYMOUS_REQUESTS:
            return response

        # IP address
        ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ip:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ip = ip.split(', ')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', None)

        # Language code
        language_code = getattr(request, 'LANGUAGE_CODE', None)

        # Timezone
        timezone = request.META.get('TZ', None)

        # User agent
        user_agent = request.META.get('HTTP_USER_AGENT', None)

        # Content type
        content_type = request.META.get('CONTENT_TYPE', None)

        # Response content
        response_content = None
        if response:
            if response.status_code == 500 and DETECTIVE_SAVE_ERROR_RESPONSES:
                #response_content = response.content # this is only useful if DEBUG is True
                # if DEBUG is False, simulate that DEBUG is enabled and get technical exception details:
                from django.views import debug
                exc_info = sys.exc_info()
                debug_response = debug.technical_500_response(request, *exc_info)
                response_content = debug_response.content
            elif response.status_code != 500 and DETECTIVE_SAVE_RESPONSES:
                response_content = response.content

        # Store to database
        try:
            TrackingLog.objects.create(
                user=user,
                request_method=request.META['REQUEST_METHOD'],
                #    remote_addr = request.META['REMOTE_ADDR'],
                ip_address=ip,
                path=request.path,
                #    query_string = request.META['QUERY_STRING'],
                #    full_path = request.get_full_path(),
                params_get=str(dict(request.GET)),
                params_post=str(dict(request.POST)),
                session=str(dict(request.session)),
                status_code=response.status_code,
                language_code=language_code,
                timezone=timezone,
                content_type=content_type,
                user_agent=user_agent,
                response=response_content,
                is_secure=request.is_secure(),
                is_ajax=request.is_ajax(),
                is_debug=DETECTIVE_DEBUG
            )
        except utils.DatabaseError:
            pass

        # Return original response
        return response
