"""Framework wide datastore models."""

from google.appengine.ext import ndb

import os

@ndb.transactional
def GetApplicationConfiguration():
  """Returns the application configuration, creating it if necessary."""
  key = ndb.Key(Config, 'config')
  entity = key.get()
  if not entity:
    entity = Config(key=key)
    entity.xsrf_key = os.urandom(16)
    entity.put()
  return entity


class Config(ndb.Model):
  """A simple key-value store for application configuration settings."""

  xsrf_key = ndb.BlobProperty()
