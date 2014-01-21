from django.contrib import admin

from models import TrackingLog


class TrackingLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['user', 'request_method', 'status_code', 'ip_address', 'path', 'params_get', 'params_post',
                    'is_secure', 'is_ajax', 'is_debug', 'created']
    list_filter = ['is_secure', 'is_ajax', 'is_debug', 'created', 'status_code', 'request_method']
    search_fields = ['session', 'user_agent', 'params_get', 'params_post', 'ip_address', 'path']

    def has_add_permission(self, request):
        return False

admin.site.register(TrackingLog, TrackingLogAdmin)
