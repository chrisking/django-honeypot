try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python <= 2.4

from django.conf import settings
from django.utils.safestring import mark_safe
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

#Email Support
from django.core.mail import EmailMultiAlternatives

fromEmail = "sales@plcpart.com"
to_spamEmail = "chris.king@kilncode.com"

def honeypot_equals(val):
    """
        Default verifier used if HONEYPOT_VERIFIER is not specified.
        Ensures val == HONEYPOT_VALUE or HONEYPOT_VALUE() if it's a callable.
    """
    expected = getattr(settings, 'HONEYPOT_VALUE', '')
    if callable(expected):
        expected = expected()
    return val == expected

def verify_honeypot_value(request, field_name):
    """
        Verify that request.POST[field_name] is a valid honeypot.

        Ensures that the field exists and passes verification according to
        HONEYPOT_VERIFIER.
    """
    verifier = getattr(settings, 'HONEYPOT_VERIFIER', honeypot_equals)
    if request.method == 'POST':
        field = field_name or settings.HONEYPOT_FIELD_NAME
        if field not in request.POST or not verifier(request.POST[field]):
            resp = render_to_string('honeypot/honeypot_error.html',
                                    {'fieldname': field})
            msg = EmailMultiAlternatives("Support Request - FROM PLCPART", request.POST.getEmailBody(), fromEmail, [to_spamEmail])
            msg.attach_alternative(render_to_response('surplusEmail.html', request.POST), 'text/html')
            msg.send()
            return HttpResponseBadRequest(resp)

def check_honeypot(func=None, field_name=None):
    """
        Check request.POST for valid honeypot field.

        Takes an optional field_name that defaults to HONEYPOT_FIELD_NAME if
        not specified.
    """
    # hack to reverse arguments if called with str param
    if isinstance(func, basestring):
        func, field_name = field_name, func

    def decorated(func):
        def inner(request, *args, **kwargs):
            response = verify_honeypot_value(request, field_name)
            if response:
                return response
            else:
                return func(request, *args, **kwargs)
        return wraps(func)(inner)

    if func is None:
        def decorator(func):
            return decorated(func)
        return decorator
    return decorated(func)
