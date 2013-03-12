from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import tch.cv.model.ext.CV


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('tch/cv/webapp/web/'))


def templateResolve(controller_name):

    templates = {'/cv' : "index.html"}
    if templates.has_key(controller_name):
        template = jinja_environment.get_template(templates.get(controller_name))
    else:
        template = jinja_environment.get_template('default')
    return template

class CreateCV(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        template_values = {
            'position_categories': tch.cv.model.ext.CV.position_categories,
        }
        self.response.out.write(templateResolve('/create').render(template_values))
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        template_values = {}
        self.response.out.write(templateResolve('/cv').render(template_values))


   
class BusinessCard(webapp.RequestHandler):
    def get(self):
       # self.response.headers['Content-Type'] = 'text/plain'
        template_values = {}
        self.response.out.write(templateResolve('/cv').render(template_values))


application = webapp.WSGIApplication([('/cv', BusinessCard), ('/cv/create', CreateCV)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

