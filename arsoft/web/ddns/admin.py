from django.contrib import admin
from arsoft.web.ddns.models import DDNSModel

class WebDDNSAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'rdtype')
    fields = ['hostname', 'password', 'rdtype']

admin.site.register(DDNSModel, WebDDNSAdmin)
