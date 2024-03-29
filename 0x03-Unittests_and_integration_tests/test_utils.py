#!/usr/bin/env python3
"""test_utils"""
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
import unittest
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Test class for utils.access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b",), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Exception test for utils.access_nested_map"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """unittest for utils.get_json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True},),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """unittest for utils.get_json"""
        mock = Mock()
        mock.json.return_value = test_payload

        with patch('requests.get', return_value=mock) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test for utils.memoize"""

    def test_memoize(self):
        """Test memoize"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass,
                          'a_method',
                          return_value=lambda: 42
                          ) as mocked:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            mocked.assert_called_once()
