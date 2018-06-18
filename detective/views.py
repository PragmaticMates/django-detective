import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView


from detective.models import TrackingLog


class JsonResponse(HttpResponse):
    def __init__(self, json_obj):
        content = json.dumps(json_obj, indent=4)
        super(JsonResponse, self).__init__(
            content=content, mimetype='application/json; charset=utf8'
        )


class TrackingLogDetailView(DetailView):
    model = TrackingLog

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active or not request.user.is_superuser:
            return HttpResponseForbidden()
        tracking_log = self.get_object()

        try:
            json_obj = json.loads(tracking_log.response)
            return JsonResponse(json_obj)
        except (TypeError, ValueError):
            return HttpResponse(tracking_log.response)
