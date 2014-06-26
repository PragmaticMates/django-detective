django-detective
================

Django app that tracks all user requests and saves following data to database:

- user
- request method
- response status code
- IP address
- URL path
- GET parameters
- POST data
- session
- language code
- timezone
- content type
- user agent
- response content (if internal server error occures)
- is_secure flag
- is_ajax flag
- is_debug flag
- created and modified timestamps


Tested on Django 1.4.5.


Requirements
------------
- Django


Installation
------------

1. Install python library using pip: ``pip install django-detective``

2. Add ``detective`` to ``INSTALLED_APPS`` in your Django settings file

3. Add ``detective.middleware.TrackingMiddleware`` to ``MIDDLEWARE_CLASSES`` in your Django settings file

4. Include ``detective.urls`` in your urls.py

5. Sync your database


Settings
''''''''

DETECTIVE_SAVE_RESPONSES
    If True, response data will be saved in database. Default: ``False``.

DETECTIVE_SAVE_ERROR_RESPONSES
    If True, internal server error responses with exception (500) are stored in database. Default: ``True``.

DETECTIVE_TRACK_AJAX_REQUESTS
    If False, ajax requests won't be tracked. Default: ``True``.

DETECTIVE_TRACK_ANONYMOUS_REQUESTS
    If False, anonymous requests won't be tracked. Default: ``True``.


Authors
-------

Library is by `Erik Telepovsky` from `Pragmatic Mates`_. See `our other libraries`_.

.. _Pragmatic Mates: http://www.pragmaticmates.com/
.. _our other libraries: https://github.com/PragmaticMates
