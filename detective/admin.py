from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import TrackingLog


class AdminPathFilter(admin.SimpleListFilter):
    title = _('admin')
    parameter_name = 'in_admin'

    def lookups(self, request, model_admin):
        return (
            ('inside', _('inside admin')),
            ('outside', _('outside admin')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'inside':
            return queryset.filter(path__contains='/admin/')
        if self.value() == 'outside':
            return queryset.exclude(path__contains='/admin/')
        return queryset


class TrackingLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['user', 'request_method', 'status_code', 'ip_address', 'path', 'params_get', 'params_post',
                    'is_secure', 'is_ajax', 'is_debug', 'created']
    list_filter = [AdminPathFilter, 'is_secure', 'is_ajax', 'is_debug', 'created', 'status_code', 'request_method']
    search_fields = ['session', 'user_agent', 'params_get', 'params_post', 'ip_address', 'path']

    def has_add_permission(self, request):
        return False

admin.site.register(TrackingLog, TrackingLogAdmin)
