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

from models import TrackingLog
from settings import DETECTIVE_TRACK_AJAX_REQUESTS, DETECTIVE_TRACK_ANONYMOUS_REQUESTS, DETECTIVE_SAVE_ERROR_RESPONSES, \
    DETECTIVE_DEBUG


class TrackingMiddleware(object):
    def process_response(self, request, response):
        # Ajax request
        if request.is_ajax() and not DETECTIVE_TRACK_AJAX_REQUESTS:
            return response

        # Currently logged in user
        try:
            user = request.user if request.user.is_authenticated() else None
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
        try:
            language_code = str(request.LANGUAGE_CODE)
        except AttributeError:
            language_code = None

        # Timezone
        #try:
        #    timezone = request.META['TZ']
        #except KeyError:
        #    timezone = None

        # User agent
        try:
            user_agent = request.META['HTTP_USER_AGENT']
        except KeyError:
            user_agent = None

        # Content type
        try:
            content_type = request.META['CONTENT_TYPE']
        except KeyError:
            content_type = None

        # Response content
        response_content = None
        if response and response.status_code == 500 and DETECTIVE_SAVE_ERROR_RESPONSES:
            #response_content = response.content # this is only useful if DEBUG is True
            # if DEBUG is False, simulate that DEBUG is enabled and get technical exception details:
            from django.views import debug
            exc_info = sys.exc_info()
            debug_response = debug.technical_500_response(request, *exc_info)
            response_content = debug_response.content

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
                #timezone=timezone,
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
