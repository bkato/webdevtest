"""Tests for base.models."""

import unittest2

import models

from google.appengine.ext import testbed


class ModelsTest(unittest2.TestCase):
  """Test cases for base.models."""

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def testConfigurationAutomaticallyGenerated(self):
    config = models.GetApplicationConfiguration()
    self.assertIsNotNone(config)
    self.assertIsNotNone(config.xsrf_key)


if __name__ == '__main__':
  unittest2.main()
