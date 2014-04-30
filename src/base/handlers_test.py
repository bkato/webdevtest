"""Tests for base.handlers."""

import exceptions
import unittest2
import webapp2

import handlers
import xsrf

from google.appengine.ext import testbed


class DummyHandler(handlers.AuthenticatedHandler):
  """Convenience class to verify successful requests."""

  def get(self):
    self._RawWrite('get_succeeded')

  def post(self):
    self._RawWrite('post_succeeded')

  def DenyAccess(self):
    self._RawWrite('access_denied')

  def XsrfFail(self):
    self._RawWrite('xsrf_fail')


class DummyAjaxHandler(handlers.BaseAjaxHandler):
  """Convenience class to verify successful requests."""

  def get(self):
    pass

  def post(self):
    pass


class DummyCronHandler(handlers.BaseCronHandler):
  """Convenience class to verify successful requests."""

  def get(self):
    self._RawWrite('get_succeeded')


class DummyTaskHandler(handlers.BaseTaskHandler):
  """Convenience class to verify successful requests."""

  def get(self):
    self._RawWrite('get_succeeded')


class HandlersTest(unittest2.TestCase):
  """Test cases for base.handlers."""

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.app = webapp2.WSGIApplication([('/', DummyHandler),
                                        ('/ajax', DummyAjaxHandler),
                                        ('/cron', DummyCronHandler),
                                        ('/task', DummyTaskHandler)])

  def _FakeLogin(self):
    """Sets up the environment to have a fake user logged in."""
    self.testbed.setup_env(
        USER_EMAIL='user@example.com',
        USER_ID='123',
        overwrite=True)

  def testHandlerCannotOverrideFinalMethods(self):

    try:

      class _(handlers.BaseHandler):

        def dispatch(self):
          pass

      self.fail('should not be able to override dispatch')
    except handlers.SecurityError, e:
      self.assertTrue(e.message.find('override restricted') != -1)

  def testAuthenticatedHandlerRequiresUser(self):

    self.assertEqual('access_denied', self.app.get_response('/').body)
    self.assertEqual('access_denied', self.app.get_response('/',
                                                            method='POST').body)
    self._FakeLogin()
    self.assertEqual('get_succeeded', self.app.get_response('/').body)

  def testXsrfProtectionFailsWithInvalidToken(self):
    self._FakeLogin()
    self.assertEqual('xsrf_fail', self.app.get_response('/',
                                                        method='POST',
                                                        POST={}).body)

  def testXsrfProtectionSucceedsWithValidToken(self):
    self._FakeLogin()

    key = handlers._GetXsrfKey()
    token = xsrf.GenerateToken(key, 'user@example.com')
    self.assertEqual('post_succeeded',
                     self.app.get_response('/',
                                           method='POST',
                                           POST={'xsrf': token}).body)

  def testAjaxGetResponsesIncludeXssiPrefix(self):
    self.assertEqual(handlers._XSSI_PREFIX, self.app.get_response('/ajax').body)

  def testAjaxPostResponsesLackXssiPrefix(self):
    self.assertEqual('', self.app.get_response('/ajax', method='POST').body)

  def testCronFailsWithoutXAppEngineCron(self):
    try:
      self.app.get_response('/cron', method='GET')
      self.fail('Cron succeeded without X-AppEngine-Cron: true header')
    except exceptions.AssertionError, e:
      # webapp2 wraps the raised SecurityError during dispatch with an
      # exceptions.AssertionError.
      self.assertTrue(e.message.find('X-AppEngine-Cron') != -1)

  def testCronSucceedsWithXAppEngineCron(self):
    headers = [('X-AppEngine-Cron', 'true')]
    self.assertEqual('get_succeeded',
                     self.app.get_response('/cron',
                                           headers=headers).body)

  def testTaskFailsWithoutXAppEngineQueueName(self):
    try:
      self.app.get_response('/task', method='GET')
      self.fail('Task succeeded without X-AppEngine-QueueName header')
    except exceptions.AssertionError, e:
      # webapp2 wraps the raised SecurityError during dispatch with an
      # exceptions.AssertionError.
      self.assertTrue(e.message.find('X-AppEngine-QueueName') != -1)

  def testTaskSucceedsWithXAppEngineQueueName(self):
    headers = [('X-AppEngine-QueueName', 'default')]
    self.assertEqual('get_succeeded',
                     self.app.get_response('/task',
                                           headers=headers).body)

if __name__ == '__main__':
  unittest2.main()
