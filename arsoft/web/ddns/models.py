from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse 
import random
import string
import os
import urllib

def generate_password():
    length = 16
    chars = string.ascii_letters + string.digits
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))
    
def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)

class DDNSZoneViewModel(models.Model):

    name = models.CharField('Name', max_length=200, unique=True)
    source_address = models.GenericIPAddressField('Source address', default='127.0.0.1', protocol='both')
    source_port = models.IntegerField('Source port', default=0)
    dnsserver = models.GenericIPAddressField('DNS server', default='127.0.0.1', protocol='both')

    class Meta:
        verbose_name = "zone view"
        verbose_name_plural = "zone views"

    def __unicode__(self):
        return '%s (%s:%i)' % (self.name, self.source_address, self.source_port)

class DDNSModel(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField('Hostname', max_length=200, unique=True, help_text='Enter full qualified domain name of the host')
    password = models.CharField('Password', max_length=200, default=generate_password)
    RDTYPE_CHOICES = (
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('MX', 'MX'),
    )
    rdtype = models.CharField('DNS record type', max_length=4, default='A', choices=RDTYPE_CHOICES)
    STATE_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('D', 'Deleted'),
    )
    state = models.CharField('State', max_length=4, default='A', choices=STATE_CHOICES)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Last updated', auto_now=True)
    zone_views = models.ManyToManyField(DDNSZoneViewModel, verbose_name="list of zone views")
    
    def zone_view_names(self):
        return "\n".join([s.name for s in self.zone_views.all()])
    zone_view_names.short_description = "Zone Views"

    class Meta:
        verbose_name = "host"
        verbose_name_plural = "hosts"

    def _get_update_url(self):
        "Returns the URL for the updating the host."
        return url_with_querystring(reverse('arsoft.web.ddns.views.update'),
                    host=self.hostname, pw=self.password)
    update_url = property(_get_update_url)
    def _get_address(self):
        "Returns the current address from the DNS for the host."
        return 'Not impl'
    address = property(_get_address)

    def __unicode__(self):
        return '%s (%s)' % (self.hostname, self.rdtype)
    