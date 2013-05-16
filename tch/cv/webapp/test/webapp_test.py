'''
Created on 27-10-2012

@author: user
'''
from tch.cv.util.test import test_utils
from tch.cv.webapp.main import BusinessCard, splitURLPath
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        
        #cv = BusinessCard()
        #cv.initialize(test_utils.mockRequest(), test_utils.mockResponse())
        
        #cv.get()
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass
    
    def testSplitURLPath(self):
        self.assertEqual(len(splitURLPath('')), 1)
        self.assertEqual(len(splitURLPath('/')), 1)
        self.assertEqual(len(splitURLPath('/1/2/3')), 3)
        self.assertEqual(len(splitURLPath('/1/2/3/')), 4)
        self.assertEqual(len(splitURLPath('/1/2/3/4')), 4)
        self.assertEqual(len(splitURLPath('/abc/def/gh11/22')), 4)
        
    def testCurrentLanguage(self):
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()