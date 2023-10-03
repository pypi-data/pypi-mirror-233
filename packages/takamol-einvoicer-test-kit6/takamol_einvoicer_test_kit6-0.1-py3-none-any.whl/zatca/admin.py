from django.contrib import admin

from zatca.models import ZatcaLog, ZatcaKey
from django.utils.safestring import mark_safe


class PermissionsModelAdmin(admin.ModelAdmin):
    """
    This class is used to unify all Admin classes permissions based on user permissions
    """

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            res = ''
            for change in delta.changes:
                res += f"<tr><td>{self.model._meta.get_field(change.field).verbose_name}</td><td>{change.old}</td><td>{change.new}</td></tr>"

            if res:
                return mark_safe(f"<table><tr><th>Field</th><th>From</th><th>To</th></tr>{res}</table>")
        return None


@admin.register(ZatcaKey)
class KeyAdmin(PermissionsModelAdmin):
    list_display = ('id', 'type', 'active', 'expiry_date', 'created_at')
    fields = (
        'id',
        'username',
        ('password', 'expiry_date',),
        ('active', 'type',),
        ('meta_data')
    )

    readonly_fields = ('id',)


@admin.register(ZatcaLog)
class LogAdmin(PermissionsModelAdmin):
    list_display = ('id', 'request_type', 'get_invoice', 'status_code', 'created_at')
    fields = (
        'id',
        'req',
        ('res', 'request_type',),
        ('get_invoice',),
    )

    readonly_fields = ('id',)

    def get_invoice(self, obj):
        return obj.invoice
