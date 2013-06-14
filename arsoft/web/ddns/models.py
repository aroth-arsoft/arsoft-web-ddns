from django.db import models
from django import forms

class DDNSModel(models.Model):
    hostname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    RDTYPE_CHOICES = (
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('MX', 'MX'),
    )
    rdtype = models.CharField(max_length=4, default='A', choices=RDTYPE_CHOICES)

    def __unicode__(self):
        return '%s (%s)' % (self.hostname, self.rdtype)
