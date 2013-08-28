from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import logging
import os.path
import datetime
import arsoft.dnsutils
import dns.update
import dns.resolver
import dns.rdatatype
import dns.rdtypes
import dns.rcode
import dns.tsig
import socket
import errno
from arsoft.web.ddns.models import DDNSModel

logger = logging.getLogger('arsoft.web.ddns')

def _check_config():
    ret = True
    errors = []
    if ret:
        dns_update_keyfile = os.path.join(settings.CONFIG_DIR, 'dns-update.key')
        if not os.path.isfile(dns_update_keyfile):
            errors.append('DNS update key %s missing' % dns_update_keyfile)
            ret = False
        elif not os.access(dns_update_keyfile, os.R_OK):
            errors.append('DNS update key %s not readable' % dns_update_keyfile)
            ret = False
    return (ret, errors)
    

def parse_name(Origin, Name):
    try:
        n = dns.name.from_text(Name)
    except:
        return None, None
    if Origin is None:
        Origin = dns.resolver.zone_for_name(n)
        Name = n.relativize(Origin)
        return Origin, Name
    else:
        try:
            Origin = dns.name.from_text(Origin)
            Name = n - Origin
        except:
            Origin = None
            Name = None
        return Origin, Name
    
def _get_update_object(self, name, keyring):
    Origin, Name = self.parse_name(Origin=None, Name=name)
    if Origin is not None:
        for update in self._updates:
            if update.origin == Origin:
                return update
        update = dns.update.Update(Origin, keyring=keyring)
        self._updates.append(update)
        return update
    return None
    

def home(request):
    response_status = 200
    response_data = 'no operation specified.'
    return HttpResponse(response_data, status=response_status, content_type="text/plain")

def _get_request_param(request, paramname, default_value=None):
    if paramname in request.GET:
        if isinstance(default_value, int):
            ret = int(request.GET[paramname])
        elif isinstance(default_value, str) or isinstance(default_value, unicode):
            ret = str(request.GET[paramname])
        else:
            ret = request.GET[paramname]
    else:
        ret = default_value
    return ret


def _get_request_meta_param(request, paramname, default_value=None):
    if paramname in request.META:
        if isinstance(default_value, int):
            ret = int(request.META[paramname])
        elif isinstance(default_value, str) or isinstance(default_value, unicode):
            ret = str(request.META[paramname])
        else:
            ret = request.META[paramname]
    else:
        ret = default_value
    return ret

def update(request):
    (config_ok, config_errors) = _check_config()
    if not config_ok:
        logger.error(config_errors)
        response_data = '\n'.join(config_errors)
        response_status = 500
    else:
        hostname = _get_request_param(request, 'host', '')
        address = _get_request_param(request, 'addr', '')
        if len(address) == 0:
            address = _get_request_meta_param(request, 'REMOTE_ADDR', '')
        password = _get_request_param(request, 'pw', '')
        if len(address):
            if 'type' in request.GET:
                rdtype = dns.rdatatype.from_text(_get_request_param(request, 'type', settings.DEFAULT_RRTYPE))
                if arsoft.dnsutils.is_valid_ipv4(address) or arsoft.dnsutils.is_valid_ipv6(address):
                    address_valid = True
                else:
                    address_valid = False
            elif arsoft.dnsutils.is_valid_ipv4(address):
                rdtype = dns.rdatatype.from_text('A')
                address_valid = True
            elif arsoft.dnsutils.is_valid_ipv6(address):
                rdtype = dns.rdatatype.from_text('AAAA')
                address_valid = True
            else:
                address_valid = False
        else:
            address_valid = False

        ttl = _get_request_param(request, 'ttl', settings.DEFAULT_TTL)

        if len(hostname) and len(password) and len(address) and address_valid:
            host_from_db = DDNSModel.objects.get(hostname=hostname)
            #print(host_from_db)
            #print(len(host_from_db))
            if host_from_db is None:
                response_data = 'Host %s not configured' % (str(hostname))
                response_status = 503
            elif host_from_db.password != password:
                response_data = 'Password for host %s does not match' % (str(hostname))
                response_status = 503
            else:
                dns_update_keyfile = os.path.join(settings.CONFIG_DIR, 'dns-update.key')
                Origin, Name = parse_name(Origin=None, Name=hostname)
                response_data = 'Update zone %s' % (Origin)
                update = dns.update.Update(Origin)
                if not arsoft.dnsutils.use_key_file(update, dns_update_keyfile, arsoft.dnsutils.KeyFileFormat.TSIG):
                    logger.error('Failed to use keyfile %s' % (dns_update_keyfile))
                else:
                    logger.error('Use dns keyalgo=%s, name=%s, ring=%s' % (update.keyalgorithm, update.keyname, update.keyring))
                logger.error('Update hostname=%s, ttl=%s, rdtype=%s, addr=%s' % (hostname, ttl, rdtype, address))
                update.replace(hostname, ttl, rdtype, address)

                try:
                    for zone_view in host_from_db.zone_views.all():
                        source_address = zone_view.source_address
                        source_port = zone_view.source_port
                        dnsserver = zone_view.dnsserver
                        response = dns.query.tcp(update, dnsserver, timeout=settings.DNS_TIMEOUT, source=source_address, source_port=zone_view.source_port)
                        #print "Return code: %i" % response.rcode()
                        rcode = response.rcode()
                        if rcode == dns.rcode.NOERROR:
                            host_from_db.update(updated=datetime.datetime.now(), address=address)
                            response_data = 'Updated %s to %s in %s' % (hostname, address, Origin)
                            response_status = 200
                        elif rcode == dns.rcode.NOTAUTH:
                            response_data = 'Not authorized to update %s to %s in %s' % (hostname, address, Origin)
                            response_status = 503
                            break
                        else:
                            response_data = 'Response code %s (%i), opcode %i: %s' % (dns.rcode.to_text(rcode), rcode, response.opcode(), response.to_text())
                            response_status = 503
                            break
                except dns.exception.Timeout:
                    response_data = 'timeout'
                    response_status = 503
                except dns.tsig.BadSignature:
                    response_data = 'BadSignature using key %s to update %s to %s in %s' % (update.keyname, hostname, address, Origin)
                    response_status = 503
                except dns.tsig.PeerBadSignature:
                    response_data = 'PeerBadSignature using key %s to update %s to %s in %s' % (update.keyname, hostname, address, Origin)
                    response_status = 503
                except dns.exception.DNSException as e:
                    response_data = 'DNS error %s %s' % (str(type(e)), str(e))
                    response_status = 503
                except socket.error as (error_num, error_msg):
                    if error_num == errno.ECONNREFUSED:
                        response_data = 'Network error: Server %s refused connection (either DNS server is down or DNS server address is wrong)' % (dnsserver)
                        response_status = 503
                    else:
                        response_data = 'Network error %i: %s' % (error_num, str(error_msg))
                        response_status = 503
        else:
            response_status = 400
            if not address_valid:
                response_data = 'given address %s is invalid.' % (str(address))
            else:
                response_data = 'missing parameter(s)'

    return HttpResponse(response_data, status=response_status, content_type="text/plain")
