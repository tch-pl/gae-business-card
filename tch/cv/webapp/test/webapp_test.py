'''
Created on 27-10-2012

@author: user
'''
import unittest
from tch.cv.webapp.pages import BusinessCard
from tch.cv.util.test import test_utils

class Test(unittest.TestCase):


    def setUp(self):
        cv = BusinessCard()
        cv.initialize(test_utils.mockRequest(), test_utils.mockResponse())
        cv.get()


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()