from django.conf.urls import url

from views import TrackingLogDetailView


urlpatterns = [
    url(r'^trackinglog/detail/(?P<pk>[-\d]+)/$', TrackingLogDetailView.as_view(), name='trackinglog_detail'),
]
