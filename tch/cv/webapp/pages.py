#-*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
from tch.cv.model.ext import CVModel

"""Author: Tomasz Chrul"""

#TODO
"""

"""


template_path = 'tch/cv/webapp/web/'
default_language = 'pl'
supported_languages = ['pl', 'en']
default_controller = 'about'
default_ajax_controller = 'ajax_certs'

class MenuItem():
    template = None
    link = None
    description = {}
    
    def __init__(self, link, template, description={}):
        self.template = template
        self.link = link
        self.description = description
        
    def getDescription(self, current_language):
        current_description = None
        if current_language is not None:
            current_description = self.description.get(current_language)
        if  current_description is None:
            current_description = self.description.get("pl")
        return current_description
        

menu = [MenuItem('about', "about.html", {"pl":"O mnie", "en":"About myself"}),
        MenuItem('employment', "employment.html", {"pl":"Zatrudnienie", "en":"Employment"}),
             MenuItem('education', "education.html", {"pl":"Edukacja", "en":"Education"}),
             MenuItem('experience', "experience_certificates.html", {"pl":u"Doświadczenie", "en":"Experience"})
             ]


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))


def templateResolve(controller_name):    
    template = None
    if controller_name is None:
        controller_name = default_controller
    for item in menu:
        if item.link == controller_name:           
            template = jinja_environment.get_template(item.template)
            break
    if template is None: 
            template = jinja_environment.get_template('index.html')
    return template

def splitURLPath(path):
    if path.startswith('/'):
        path = path.lstrip('/')
    splitted_path = path.split('/')
    return splitted_path
   # if len(splitted_path) > 2:
    #    return [splitted_path[0], splitted_path[1], splitted_path[2]]        
    #elif len(splitted_path) > 1:
     #   return [splitted_path[0], splitted_path[1]]
    
def isLanguageSupported(language):
    
    if language in supported_languages:
        return True
    
    return False

#class CreateCV(webapp.RequestHandler):
#    def get(self):
#        self.response.headers['Content-Type'] = 'text/plain'
#        template_values = {
#            'position_categories': tch.cv.model.ext.CV.position_categories,
#        }
#        self.response.out.write(templateResolve('/create').render(template_values))
#        
#    def post(self):
#        self.response.headers['Content-Type'] = 'text/plain'
#        template_values = {}
#        self.response.out.write(templateResolve('/cv').render(template_values))

class Main(webapp.RequestHandler):
    def get(self):
        self.redirect("/cv")


   
class BusinessCard(webapp.RequestHandler):
    def get(self):
        splitted = splitURLPath(self.request.path)        
        language = default_language
        if splitted is not None and len(splitted) > 1 and isLanguageSupported(splitted[1]):
            language = splitted[1]                
        controller_name = None
        if splitted is not None and len(splitted) == 3:
            controller_name = splitted[2]
        else:
            controller_name = default_controller    
        template_values = self.resolveModel(language, controller_name) 
        self.response.out.write(templateResolve(controller_name).render(template_values))

    def resolveModel(self, language, controller_name):
        content = self.resolveContent(controller_name)
        title = {'pl': u'Trochę informacji o mnie', 'en': 'Some info about me'}
        since_date = {'pl': 'Od', 'en': 'Since'}
        to_date = {'pl': 'Do', 'en': 'To'}
        
        model = {
                 'menu' : menu,
                 'language' : language,
                 'title' : title,
                 'supported_languages' : supported_languages,
                 'content' : content,
                 'controller_name' : controller_name,
                 'since_date' : since_date[language],
                 'to_date' : to_date[language]
                 }
        return model
    
    def resolveContent(self, controller_name, user=""):
        controlled_content = CVModel.CVContentFactory().generateContent(controller_name)
        main_content = {"profession": "Software Engineer",
                 "full_name" : "Tomasz Chrul"}
        
        content = main_content.copy()
        content.update(controlled_content)                                        
        return content

class CVRPCHandler(webapp.RequestHandler):
    """ Will handle the RPC requests."""
    def get(self):
        
        splitted = splitURLPath(self.request.path)        
        language = default_language
        if splitted is not None and len(splitted) > 1 and isLanguageSupported(splitted[1]):
            language = splitted[1]                
        controller_name = None
        if splitted is not None and len(splitted) == 4:
            controller_name = splitted[2] + "_" +splitted[3]
        else:
            controller_name = default_ajax_controller    
        #template_values = self.resolveModel(language, controller_name) 
        #self.response.out.write(templateResolve(controller_name).render(template_values))        
        self.response.out.write(splitted)


    
application = webapp.WSGIApplication([('/', Main), (r'/cv.*/ajax.*', CVRPCHandler), (r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
   CVModel.HistoryContent()
