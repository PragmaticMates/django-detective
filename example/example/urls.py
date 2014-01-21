from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from views import ViewA, ViewB, ViewC


admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    url(r'^view-C/$', ViewC.as_view(), name='view_c'),
    url(r'^view-B/$', ViewB.as_view(), name='view_b'),
    url(r'^view-A/$', ViewA.as_view(), name='view_a'),
    url(r'^$', ViewA.as_view(), name='home'),
)
