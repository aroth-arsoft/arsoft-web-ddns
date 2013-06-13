from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

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

    title = 'Change password service'

    t = loader.get_template('home.html')
    c = RequestContext( request, { 
        'errormessage':error_message, 
        'statusmessage':status_message,
        'username':username,
        'title':title
        })
    return HttpResponse(t.render(c))

def update(request):
    try:
        username = request.POST['username']
        oldpassword = request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        confpassword = request.POST['confpassword']
    except KeyError:
        error_message = 'Insufficient data.'
        username = None
        pass
        
    if username:
        if newpassword != confpassword:
            error_message = 'New password and confirmation password do not match.'
            result_code = False
        elif oldpassword == '':
            error_message = 'Current password not specified.'
            result_code = False
        elif newpassword == '':
            error_message = 'No new password specified.'
            result_code = False
        else:
            (ret, error_message) = kpasswd(username, oldpassword, newpassword)
            if ret:
                error_message = 'Successful.'
                result_code = True
            else:
                error_message = 'Failed to change password. ' + error_message
                result_code = False
    else:
        error_message = 'No user name specified.'
        result_code = False


    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    request.session['username'] = username
    request.session['error_message'] = error_message
    request.session['result'] = result_code
    return HttpResponseRedirect(reverse('arsoft.web.update.views.home'))
