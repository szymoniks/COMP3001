#!/usr/bin/python
import random
import unittest

class TestXMLWriter(unittest.TestCase):

  def setUp(self):
    self.random_strings = []
    for x in range(0,100):
      random_strings.append(''.join(random.choice('0123456789ABCDEF') for i in range(16)))

  ## Unittest to generate XML format
  #
  # Attributes are constant
  #
  def test_generate_xml(self):
    for string in random_strings:
