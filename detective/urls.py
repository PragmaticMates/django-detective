from django.conf.urls import patterns, url

from views import TrackingLogDetailView


urlpatterns = patterns('',
    url(r'^trackinglog/detail/(?P<pk>[-\d]+)/$', TrackingLogDetailView.as_view(), name='trackinglog_detail'),
)
