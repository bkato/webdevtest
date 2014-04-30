"""Public constants for use in application configuration."""

import os


def _IsDebug():
  return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

# webapp2 application configuration constants.
# template
(DJANGO, JINJA2) = range(0, 2)

# using_angular
DEFAULT_ANGULAR = False

# framing_policy
(DENY, SAMEORIGIN, PERMIT) = range(0, 3)
X_FRAME_OPTIONS_VALUES = {DENY: 'DENY', SAMEORIGIN: 'SAMEORIGIN'}

# hsts_policy
DEFAULT_HSTS_POLICY = {'max_age': 2592000, 'includeSubdomains': True}

# csp_policy
DEFAULT_CSP_POLICY = {'default-src': '\'self\''}

DEBUG = _IsDebug()
TEMPLATE_DIR = os.path.sep.join([os.path.dirname(__file__), '..', 'templates'])
