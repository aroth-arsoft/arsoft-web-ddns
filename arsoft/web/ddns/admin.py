from django.contrib import admin
from django import forms
from arsoft.web.ddns.models import DDNSModel, DDNSZoneViewModel

class WebDDNSForm(forms.ModelForm):
    class Meta:
        model = DDNSModel

class WebDDNSAdmin(admin.ModelAdmin):

    list_display = ('hostname', 'state', 'rdtype', 'user', 'address', 'zone_view_names', 'created', 'updated')
    fields = ['user', 'state', 'hostname', 'password', 'rdtype', 'address', 'update_url', 'zone_views']
    readonly_fields = ('updated', 'created', 'address', 'update_url')
    form = WebDDNSForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(WebDDNSAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DDNSModel, WebDDNSAdmin)


class WebDDNSZoneViewForm(forms.ModelForm):
    class Meta:
        model = DDNSZoneViewModel

class WebDDNSZoneViewAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_address', 'source_port', 'dnsserver')
    fields = ['name', 'source_address', 'source_port', 'dnsserver']
    form = WebDDNSZoneViewForm

admin.site.register(DDNSZoneViewModel, WebDDNSZoneViewAdmin)
