#!/usr/bin/env python3
import unittest
import reggie
import reggie.__main__


class TestReggie(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test___main__(self):
        reggie.__main__
