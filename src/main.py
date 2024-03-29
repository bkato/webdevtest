"""Main application entry point."""

import base.api_fixer

import webapp2

import base
import base.constants
import handlers


# These should all inherit from base.handlers.BaseHandler
_UNAUTHENTICATED_ROUTES = [('/', handlers.RootHandler),
                           ('/xss', handlers.XssHandler),
                           ('/xssi', handlers.XssiHandler)]

# These should all inherit from base.handlers.BaseAjaxHandler
_UNAUTHENTICATED_AJAX_ROUTES = [('/csp', handlers.CspHandler)]

# These should all inherit from base.handlers.AuthenticatedHandler
_USER_ROUTES = [('/xsrf', handlers.XsrfHandler)]

# These should all inherit from base.handlers.AuthenticatedAjaxHandler
_AJAX_ROUTES = []

# These should all inherit from base.handlers.AdminHandler
_ADMIN_ROUTES = []

# These should all inherit from base.handlers.AdminAjaxHandler
_ADMIN_AJAX_ROUTES = []

# These should all inherit from base.handlers.BaseCronHandler
_CRON_ROUTES = []

# These should all inherit from base.handlers.BaseTaskHandler
_TASK_ROUTES = []

# Place global application configuration settings here.
# These values will be accessible from handler methods like this:
# self.app.config.get('foo')
# Framework level settings:
#   template: one of base.constants.JINJA2 (default) or base.constants.DJANGO.
#
#   using_angular: True or False (default).  When True, an XSRF-TOKEN cookie
#                  will be set for interception/use by Angular's $http service.
#                  When False, no header will be set (but an XSRF token will
#                  still be available under the _xsrf key for Django/Jinja
#                  templates).
#
#   framing_policy: one of base.constants.DENY (default),
#                   base.constants.SAMEORIGIN, or base.constants.PERMIT
#
#   hsts_policy:    A dictionary with minimally a 'max_age' key, and optionally
#                   a 'includeSubdomains' boolean member.
#                   Default: { 'max_age': 2592000, 'includeSubDomains': True }
#                   implying 30 days of strict HTTPS for all subdomains.
#
#   csp_policy:     A dictionary with keys that correspond to valid CSP
#                   directives, as defined in the W3C CSP 1.1 spec.  Each
#                   key/value pair is transmitted as a distinct
#                   Content-Security-Policy header.
#                   Default: {'default-src': '\'self\''}
#                   which is a very restrictive policy.  An optional
#                   'reportOnly' boolean key substitutes a
#                   'Content-Security-Policy-Report-Only' header
#                   name in lieu of 'Content-Security-Policy' (the default
#                   is base.constants.DEBUG).
#
#  Note that the default values are also configured in app.yaml for files
#  served via the /static/ resources.  You may need to change the settings
#  there as well.

_CONFIG = {
    # Developers are encouraged to build sites that comply with this (or
    # a similarly restrictive) CSP policy.  In particular, adding directives
    # such as unsafe-inline or unsafe-eval is highly discouraged, as these
    # may lead to XSS attacks.
    'csp_policy': {
        # https://developers.google.com/fonts/docs/technical_considerations
        'font-src':    '\'self\' themes.googleusercontent.com '
                       'fonts.gstatic.com',
        # Maps, YouTube provide <iframe> based embedding at these URIs.
        'frame-src':   '\'self\' www.google.com www.youtube.com',
        # Static content.
        'img-src':     '\'self\' *.gstatic.com',
        # Assorted Google-hosted APIs.
        'script-src':  '\'self\' *.googleapis.com '
                       '*.googleanalytics.com *.google-analytics.com '
                       'apis.google.com www.google.com *.gstatic.com',
        # In generated code from http://www.google.com/fonts
        'style-src':   '\'self\' fonts.googleapis.com',
        # Fallback.
        'default-src': '\'self\'',
        'report-uri':  '/csp',
        'reportOnly': base.constants.DEBUG,
        }
    }

###############################################################################
# DO NOT MODIFY BELOW THIS LINE WITHOUT CONSULTING YOUR SECURITY TEAM CONTACT #
###############################################################################

# TODO(philames): add a verification pass here (or via a linter) which ensures
# that the handlers in the specified routes all inherit from one of our approved
# base classes.

app = webapp2.WSGIApplication(
    routes=(_UNAUTHENTICATED_ROUTES + _UNAUTHENTICATED_AJAX_ROUTES +
            _USER_ROUTES + _AJAX_ROUTES + _ADMIN_ROUTES + _ADMIN_AJAX_ROUTES +
            _CRON_ROUTES + _TASK_ROUTES),
    debug=base.constants.DEBUG,
    config=_CONFIG)
