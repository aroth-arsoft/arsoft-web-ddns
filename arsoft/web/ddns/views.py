from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import json
import logging
import os.path
import arsoft.dns
import dns.update
import dns.resolver

logger = logging.getLogger('arsoft.web.ddns')

def _check_config():
    ret = True
    errors = []
    if ret:
        dns_update_keyfile = os.path.join(settings.CONFIG_DIR, 'dns-update.key')
        if not os.path.isfile(dns_update_keyfile):
            errors.append('DNS update key %s missing' % dns_update_keyfile)
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
    try:
        username = request.session['username']
        result = request.session['result']
        if result:
            status_message = request.session['error_message']
            error_message = ''
        else:
            error_message = request.session['error_message']
            status_message = ''
    except (KeyError):
        error_message = ''
        status_message = ''
        username = ''
        pass

    if 'REMOTE_USER' in request.META:
        username = request.META['REMOTE_USER']
    if 'HTTP_AUTHORIZATION' in request.META:
        username = request.META['HTTP_AUTHORIZATION']

    response_data = {}
    response_data['error'] = 'no operation specified.'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def update(request):
    response_data = {}

    logger.warning('update req')
    (config_ok, config_errors) = _check_config()
    if not config_ok:
        logger.error(config_errors)
        response_data['error'] = config_errors
        return HttpResponse(json.dumps(response_data), status=500, content_type="application/json")

    try:
        hostname = request.GET['host']
        address = request.GET['addr']
        rrtype = request.GET['type']
        password = request.GET['pw']
    except KeyError as e:
        error_message = 'Missing parameter %s' % (str(e))
        hostname = None
        pass
        
    if hostname:
        dns_update_keyfile = os.path.join(settings.CONFIG_DIR, 'dns-update.key')
        error_message = 'All ok.'
        keyring = arsoft.dns.read_key_file(dns_update_keyfile)
        Origin, Name = parse_name(Origin=None, Name=hostname)
        update = dns.update.Update(Origin, keyring=keyring)
    else:
        error_message = 'No user name specified.'
        result_code = False

    response_data = {}
    response_data['error'] = error_message
    return HttpResponse(json.dumps(response_data), content_type="application/json")
