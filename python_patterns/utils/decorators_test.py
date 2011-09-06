#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === python_patterns.utils.decorators_test -------------------------------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
# as an unpublished work.
#
# RokuSigma Inc. (the “Company”) Confidential
#
# NOTICE: All information contained herein is, and remains the property of the
# Company. The intellectual and technical concepts contained herein are
# proprietary to the Company and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from the
# Company. Access to the source code contained herein is hereby forbidden to
# anyone except current Company employees, managers or contractors who have
# executed Confidentiality and Non-disclosure agreements explicitly covering
# such access.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of the
# Company. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE,
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS
# WRITTEN CONSENT OF THE COMPANY IS STRICTLY PROHIBITED, AND IN VIOLATION OF
# APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF
# THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
# USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
# ===----------------------------------------------------------------------===

# Python standard library, unit-testing
import unittest2

# Python patterns, scenario unit-testing
import python_patterns.unittest.scenario

# Python patterns, @Property idiom test
from python_patterns.utils.decorators import Property

##
# Constant values for the test cases in this file. INITIAL_VALUE, RESET_VALUE,
# and DELETED_VALUE must be unique from each other.
#
#   INITIAL_VALUE
#     The value initially held by the property upon creation. It is assigned
#     to the internal property _value attribute by the class constructor.
#
#   RESET_VALUE
#     The value assigned to the property during tests of the set-property
#     funcationality.
#
#   DELETED_VALUE
#     The value assigned to the property when it is deleted in the test cases
#     below. Normally of course deleting a property will have the affect to
#     destroying the object it references, removing the value from a larger
#     object, or somethng similar. But testing whether an object has been
#     deleted is difficult if not impossible to do reliably, and not really
#     the concern here. What we really want to test is much simpler: does
#     calling `del property` cause the `fdel()` method to be executed.
#
#   DOCSTRING_VALUE
#     A value which becomes the docstring for the test properties. It's real
#     value is in making sure that docstrings are being properly set in all
#     the various test scenarios, and that unicode is passed through correctly
#     without getting mangled.
#
#     NOTE: Unfortunately specifying the docstring in advance, like this, gets
#           in the way of testing the way docstrings are actually used, in-
#           line. For that reason the docstring text is repeated below,
#           verbatim in each instance that it is used. If you change the
#           DOCSTRING_VALUE, be sure to do a search and replace to find the
#           other occurrences!
INITIAL_VALUE = 3.14
RESET_VALUE = dict(a=1,b="str",c=['x','y','z'])
DELETED_VALUE = None
DOCSTRING_VALUE = u"「Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich」と言いました。"

class Getter(object):
  """
  Has a single read-only attribute, test_attrib, which returns INITIAL_VALUE.
  """
  @Property
  def test_attrib():
    u"「Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich」と言いました。"
    def fget(self):
      return self._value
    return locals()
  def __init__(self):
    self._value = INITIAL_VALUE

class TestGetter(unittest2.TestCase):
  """
  Tests existence of a docstring and reads from Getter.test_attrib.
  """

  def setUp(self):
    self._obj = Getter()

  def test_docstring(self):
    self.assertEqual(Getter.test_attrib.__doc__, DOCSTRING_VALUE)

  def test_getter(self):
    self.assertEqual(self._obj.test_attrib, INITIAL_VALUE)

class GetAndSetter(object):
  """
  Has a single read-write attribute, test_attrib, which is initialized to
  INITIAL_VALUE.
  """
  @Property
  def test_attrib():
    u"「Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich」と言いました。"
    def fget(self):
      return self._value
    def fset(self, value):
      self._value = value
    return locals()
  def __init__(self):
    self._value = INITIAL_VALUE

class TestSetter(unittest2.TestCase):
  """
  Tests existence of a docstring, reads from, and writes to
  GetAndSetter.test_attrib.
  """
  __metaclass__ = python_patterns.unittest.scenario.ScenarioMeta

  def setUp(self):
    self._obj = GetAndSetter()

  def test_docstring(self):
    self.assertEqual(GetAndSetter.test_attrib.__doc__, DOCSTRING_VALUE)

  def test_getter(self):
    self.assertEqual(self._obj.test_attrib, INITIAL_VALUE)

  class test_setter(python_patterns.unittest.scenario.ScenarioTest):
    scenarios = [
      dict(value=None),
      dict(value=0),
      dict(value=1),
      dict(value=3.14159),
      dict(value="abc"),
      dict(value=u"Zwölf Boxkämpfer"),
      dict(value=u"こんにちは"),
      dict(value=[1, 2, 3]),
      dict(value=dict(a=1, b=2, c=3)),
    ]
    def __test__(self, value):
      self._obj.test_attrib = value
      self.assertIs(self._obj.test_attrib, value)

class GetSetAndDeller(object):
  """
  Has a single read-write attribute, test_attrib, which is initialized to
  INITIAL_VALUE and can be deleted--deleting assigns DELETED_VALUE to
  test_attrib.
  """
  @Property
  def test_attrib():
    u"「Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich」と言いました。"
    def fget(self):
      return self._value
    def fset(self, value):
      self._value = value
    def fdel(self):
      self._value = DELETED_VALUE
    return locals()
  def __init__(self):
    self._value = INITIAL_VALUE

class TestDeller(unittest2.TestCase):
  """
  Tests existence of a docstring, reads from, writes to, and delete requests
  for GetSetAndDeller.test_attrib.
  """
  def setUp(self):
    self._obj = GetSetAndDeller()

  def test_docstring(self):
    self.assertEqual(GetSetAndDeller.test_attrib.__doc__, DOCSTRING_VALUE)

  def test_getter(self):
    self.assertEqual(self._obj.test_attrib, INITIAL_VALUE)

  def test_setter(self):
    self._obj.test_attrib = RESET_VALUE
    self.assertIs(self._obj.test_attrib, RESET_VALUE)

  def test_deller(self):
    del self._obj.test_attrib
    self.assertEqual(self._obj.test_attrib, DELETED_VALUE)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
