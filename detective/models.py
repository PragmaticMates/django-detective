import ast
import urllib

try:
    # Django < 2.0 support
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Django 1.5 support, falls back to auth.User to transparently work with <1.5
try:
    from django.conf import settings
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class TrackingLog(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), on_delete=models.CASCADE,
        blank=True, null=True, default=None)
    request_method = models.CharField(max_length=16, verbose_name=_(u'request method'))
#    remote_addr = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(verbose_name=_(u'IP address'), db_index=True,
        blank=True, null=True, default=None)
    path = models.CharField(max_length=1024, verbose_name=_(u'path'), db_index=True)
#    query_string = models.CharField(max_length=255)
#    full_path = models.CharField(max_length=255)
    params_get = models.TextField(verbose_name=_(u'GET params'))
    params_post = models.TextField(verbose_name=_(u'POST params'))
    session = models.TextField(verbose_name=_(u'session'))
    status_code = models.SmallIntegerField(verbose_name=_(u'status code'))
    language_code = models.CharField(max_length=2, verbose_name=_(u'language code'),
        blank=True, null=True, default=None)
    timezone = models.CharField(max_length=128, verbose_name=_(u'timezone'),
        blank=True, null=True, default=None)
    content_type = models.CharField(max_length=128, verbose_name=_(u'content type'),
        blank=True, null=True, default=None)
    user_agent = models.CharField(max_length=1024, verbose_name=_(u'user agent'),
        blank=True, null=True, default=None)
    response = models.TextField(verbose_name=_(u'response'),
        blank=True, null=True, default=None)
    is_secure = models.BooleanField(verbose_name=_(u'secure'))
    is_ajax = models.BooleanField(verbose_name=_(u'ajax'))
    is_debug = models.BooleanField(verbose_name=_(u'debug'))
    created = models.DateTimeField(verbose_name=_(u'created'), auto_now_add=True, db_index=True)
    modified = models.DateTimeField(verbose_name=_(u'modified'), auto_now=True)

    class Meta:
        db_table = 'detective_trackinglogs'
        verbose_name = _(u'tracking log')
        verbose_name_plural = _(u'tracking logs')
        ordering = ('-created', )

    def get_absolute_url(self):
        return reverse('detective:trackinglog_detail', args=(self.pk, ))

    @property
    def full_path(self):
        return u'%s?%s' % (self.path, self.query_string) if self.query_string else self.path

    @property
    def query_string(self):
        get_params = ast.literal_eval(self.params_get)
        query_pairs = [(k, v) for k, vlist in get_params.iteritems() for v in vlist]
        return urllib.urlencode(query_pairs)
