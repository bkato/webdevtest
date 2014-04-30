"""Tests for base.api_fixer."""

import json
import pickle
import unittest2
import yaml

import api_fixer


class BadPickle(object):
  """Dummy object."""
  def __reduce__(self):
    return tuple([eval, tuple(['[1][2]'])])


class ApiFixerTest(unittest2.TestCase):
  """Test cases for base.api_fixer."""

  def testJsonEscaping(self):
    o = {'foo': '<script>alert(1);</script>'}
    self.assertFalse('<' in json.dumps(o))

  def testYamlLoading(self):
    unsafe = '!!python/object/apply:os.system ["ls"]'
    try:
      yaml.load(unsafe)
      self.fail('loading unsafe YAML object succeeded')
    except yaml.constructor.ConstructorError:
      pass

  def testPickle(self):
    b = BadPickle()
    s = pickle.dumps(b)
    try:
      b = pickle.loads(s)
    except IndexError:
      self.fail('pickled code execution')
    except api_fixer.ApiSecurityException:
      pass

    try:
      b = pickle.loads(s, src_is_trusted_data=True)
    except IndexError:
      pass
    except api_fixer.ApiSecurityException:
      self.fail('should allow unsafe pickling when declared')


if __name__ == '__main__':
  unittest2.main()
