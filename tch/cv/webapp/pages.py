#-*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import json
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

default_template = "about.html"
default_ajax_template = 'empty_dynamic_content.html'

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
             MenuItem('experience', "experience.html", {"pl":u"Doświadczenie", "en":"Experience"})
             ]


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))




def splitURLPath(path):
    if path.startswith('/'):
        path = path.lstrip('/')
    splitted_path = path.split('/')
    return splitted_path
   # if len(splitted_path) > 2:
    #    return [splitted_path[0], splitted_path[1], splitted_path[2]]        
    #elif len(splitted_path) > 1:
     #   return [splitted_path[0], splitted_path[1]]

def currentLanguage(config):
    language = default_language
    if config is not None and len(config) > 1 and isLanguageSupported(config[1]):
        language = config[1]
    return language

def isLanguageSupported(language):
    if language in supported_languages:
        return True
    return False

def currentController(config):
    controller_name = default_controller 
    if config is not None and len(config) == 3:
        controller_name = config[2]
    return controller_name

def currentAjaxController(config):
    controller_name = default_ajax_controller 
    if config is not None and len(config) == 4:
            controller_name = config[2] + "_" +config[3]
    return controller_name
        
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
        language = currentLanguage(splitted)
        controller_name = currentController(splitted)
        
        template_values = self.resolveModel(language, controller_name) 
        self.response.out.write(self.templateResolve(controller_name).render(template_values))

    def resolveModel(self, language, controller_name):
        content = self.resolveContent(controller_name)
        title = {'pl': u'Trochę informacji o mnie', 'en': 'Some info about me'}
        since_date = {'pl': 'Od', 'en': 'Since'}
        to_date = {'pl': 'Do', 'en': 'To'}
        main_content = json.load(open('data/main_content.json', 'r'))
        model = {
                 'menu' : menu,
                 'language' : language,
                 'title' : title,
                 'supported_languages' : supported_languages,
                 'content' : content,
                 'main_content' : main_content,
                 'controller_name' : controller_name,
                 'since_date' : since_date[language],
                 'to_date' : to_date[language]
                 }
        return model
    
    def resolveContent(self, controller_name, user=""):
        controlled_content = CVModel.CVContentFactory().generateContent(controller_name)
        return controlled_content
    
    def templateResolve(self, controller_name):    
        template = jinja_environment.get_template(default_template)
        for item in menu:
            if item.link == controller_name:           
                template = jinja_environment.get_template(item.template)
                break
        return template

class CVRPCHandler(webapp.RequestHandler):
    
    """ Will handle the RPC requests."""
    def get(self):        
        splitted = splitURLPath(self.request.path)        
        language = currentLanguage(splitted)
        controller_name = currentAjaxController(splitted)
        template_values = self.resolveModel(language, controller_name) 
        self.response.out.write(self.templateResolve(controller_name).render(template_values))        

    def resolveModel(self, language, controller_name):
        content = self.resolveContent(controller_name)     
        model = {
                 'language' : language,
                 'supported_languages' : supported_languages,
                 'content' : content,                
                 'controller_name' : controller_name
                 }
        return model
    
    def resolveContent(self, controller_name, user=""):
        controlled_content = CVModel.CVExperienceContentFactory().generateContent(controller_name)
        return controlled_content

    def templateResolve(self, controller_name):    
        template = jinja_environment.get_template(default_ajax_template)
        for item in menu:
            if item.link == controller_name:           
                template = jinja_environment.get_template(item.template)
                break
        return template
    
application = webapp.WSGIApplication([('/', Main), (r'/cv.*/ajax.*', CVRPCHandler), (r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
   CVModel.HistoryContent()
