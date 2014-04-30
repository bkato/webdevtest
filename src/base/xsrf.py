"""Utilities related to Cross-Site Request Forgery protection."""

import hashlib
import hmac
import time

DELIMITER_ = ':'
DEFAULT_TIMEOUT_ = 86400


def _Compare(a, b):
  """Compares a and b in constant time and returns True if they are equal."""
  if len(a) != len(b):
    return False
  result = 0
  for x, y in zip(a, b):
    result |= ord(x) ^ ord(y)

  return result == 0


def GenerateToken(key, user, action='*', now=None):
  """Generates an XSRF token for the provided user and action."""
  # TODO(philames): reject cases where 'now' > int(time.time()) to prevent
  # minting tokens that don't expire for ages?
  token_timestamp = now or int(time.time())
  message = DELIMITER_.join([user, action, str(token_timestamp)])
  digest = hmac.new(key, message, hashlib.sha1).hexdigest()
  return DELIMITER_.join([str(token_timestamp), digest])


def ValidateToken(key, user, token, action='*', max_age=DEFAULT_TIMEOUT_):
  """Validates the provided XSRF token."""
  if not token or not user:
    return False
  try:
    (timestamp, digest) = token.split(DELIMITER_)
  except ValueError:
    return False
  expected = GenerateToken(key, user, action, timestamp)
  (_, expected_digest) = expected.split(DELIMITER_)
  now = int(time.time())
  if _Compare(expected_digest, digest) and now < int(timestamp) + max_age:
    return True
  return False
