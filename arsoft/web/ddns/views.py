from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
import json

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
        error_message = 'All ok.'
    else:
        error_message = 'No user name specified.'
        result_code = False

    response_data = {}
    response_data['error'] = error_message
    return HttpResponse(json.dumps(response_data), content_type="application/json")
