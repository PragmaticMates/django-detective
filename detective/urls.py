from django.conf.urls import url

from detective.views import TrackingLogDetailView

app_name = 'detective'

urlpatterns = [
    url(r'^trackinglog/detail/(?P<pk>[-\d]+)/$', TrackingLogDetailView.as_view(), name='trackinglog_detail'),
]
