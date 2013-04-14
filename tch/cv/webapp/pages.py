#-*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import json
import logging
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
        if isLanguageSupported(current_language):
            return self.description.get(current_language)
        return self.description.get(default_language)
        

menu = [MenuItem('about', "about.html", {"pl":"O mnie", "en":"About myself"}),
        MenuItem('employment', "employment.html", {"pl":"Zatrudnienie", "en":"Employment"}),
             MenuItem('education', "education.html", {"pl":"Edukacja", "en":"Education"}),
             MenuItem('experience', "experience.html", {"pl":u"Doświadczenie", "en":"Experience"})
             ]

experience = [MenuItem('ajax_certs', "experience_certs.html"),
              MenuItem('ajax_skills', "experience_skills.html")]



jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))


def splitURLPath(path):
    if path.startswith('/'):
        path = path.lstrip('/')
    splitted_path = path.split('/')
    return splitted_path

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
    if config is not None and len(config) > 3:
            controller_name = config[3] + "_" +config[4]
    return controller_name
        

class Main(webapp.RequestHandler):
    def get(self):
        self.redirect("/cv")

   
class BusinessCard(webapp.RequestHandler):
    def get(self):
        splitted = splitURLPath(self.request.path)        
        language = currentLanguage(splitted)
        controller_name = currentController(splitted)
        logging.info("Template lookup for: " + controller_name)
        template_values = self.resolveModel(language, controller_name)
        self.response.out.write(self.templateResolve(controller_name).render(template_values))

    def resolveModel(self, language, controller_name):
        content = self.resolveContent(controller_name)
        title = {'pl': u'Trochę informacji o mnie', 'en': 'Some info about me'}
        since_date = {'pl': 'Od', 'en': 'Since'}
        to_date = {'pl': 'Do', 'en': 'To'}
        main_content = json.load(open('data/main_content.json', 'r'))
        logging.info(content)
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
        logging.info(self.request.path)
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
        logging.info(content)
        return model
    
    def resolveContent(self, controller_name, user=""):
        controlled_content = CVModel.CVExperienceContentFactory().generateContent(controller_name)
        return controlled_content

    def templateResolve(self, controller_name):
        logging.info("Template lookup for: " + controller_name)
        template = jinja_environment.get_template(default_ajax_template)
        for item in experience:
            if item.link == controller_name:           
                template = jinja_environment.get_template(item.template)
                break
        return template
    
application = webapp.WSGIApplication([('/', Main), (r'/cv.*/ajax.*', CVRPCHandler), (r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
   CVModel.HistoryContent()
