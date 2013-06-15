from django.contrib import admin
from django import forms
from arsoft.web.ddns.models import DDNSModel

class WebDDNSForm(forms.ModelForm):
    class Meta:
        model = DDNSModel

class WebDDNSAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'state', 'rdtype', 'user', 'created', 'updated')
    fields = ['user', 'state', 'hostname', 'password', 'rdtype', 'update_url']
    readonly_fields = ('updated', 'created', 'update_url')
    form = WebDDNSForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(WebDDNSAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DDNSModel, WebDDNSAdmin)
