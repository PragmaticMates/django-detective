from django.contrib import admin

try:
    from django.contrib.admin.util import flatten_fieldsets
except ImportError:
    from django.contrib.admin.utils import flatten_fieldsets

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
    readonly_fields = ("created", 'modified', 'path')
    date_hierarchy = 'created'
    list_display = ['pk', 'user', 'request_method', 'status_code', 'ip_address', 'path', 'params_get', 'params_post',
                    'is_secure', 'is_ajax', 'is_debug', 'created']
    list_filter = [AdminPathFilter, 'is_secure', 'is_ajax', 'is_debug', 'created', 'status_code', 'request_method', 'user']
    search_fields = ['session', 'user_agent', 'params_get', 'params_post', 'ip_address', 'path']
    fields = (
        ('created', 'modified'),
        ('request_method', 'path', 'status_code'),
        ('is_secure', 'is_ajax', 'is_debug'),
        ('params_get',),
        ('params_post',),
        ('session',),
        ('user', 'ip_address', 'user_agent'),
        ('language_code', 'timezone',),
        ('content_type',),
        ('response',),
    )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        try:
            declared_fieldsets = self.declared_fieldsets
        except AttributeError:
            declared_fieldsets = False

        if declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

admin.site.register(TrackingLog, TrackingLogAdmin)
