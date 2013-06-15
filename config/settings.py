#!/usr/bin/python

# Put in here your custom (site-specific) settings.

# E.g. set a custum MEDIA_URLs
# settings_obj.MEDIA_URL = '/mymedia'

# Set custom source for the DDNS updates (e.g. 192.168.1.1)
settings_obj.DNS_QUERY_SOURCE = '*'

# let dnspython decide which port to use
settings_obj.DNS_QUERY_SOURCE_PORT = 0

#
# EOF
#
