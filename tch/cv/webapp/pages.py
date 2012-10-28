from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import tch.cv.model.CV

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def templateResolve(controller_name):
    path = os.path.dirname(__file__) + '\\web\\'
    
    templates = {'/create' : 'C:\\Users\\user\\workspace\\gae-business-card\\tch\\cv\\webapp\\web\\    create.html', 'default':os.path.join(path,'index.html')}
    if templates.has_key(controller_name):
        template = jinja_environment.get_template(templates.get(controller_name))
    else:
        template = jinja_environment.get_template('default')
    return template

class CreateCV(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        print os.path.dirname
        template_values = {
            'position_categories': tch.cv.model.CV.position_categories,
        }
        self.response.out.write(templateResolve('/create').render(template_values))
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        template_values = {}
        self.response.out.write(templateResolve('/cv').render(template_values))


   
class BusinessCard(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        template_values = {}
        self.response.out.write(templateResolve('/cv').render(template_values))


application = webapp.WSGIApplication([('/', CreateCV), ('/tch-business-card', BusinessCard)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

