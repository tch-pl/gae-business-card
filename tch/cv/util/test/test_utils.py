from google.appengine.ext import webapp
from StringIO import StringIO

'''
Created on 27-10-2012

@author: user
'''


def mockRequest():
    return webapp.Request({
            "wsgi.input": StringIO(),
            "CONTENT_LENGTH": 0,
            "METHOD": "GET",
                            "PATH_INFO": "/",
        })
        
def mockResponse():
    return webapp.Response()