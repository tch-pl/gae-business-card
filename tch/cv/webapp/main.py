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

''' CONFIGURATION PARAMETERS'''
template_path = 'tch/cv/webapp/web/'
default_language = 'pl'
supported_languages = ['pl', 'en']
default_controller = 'about'
default_ajax_controller = 'ajax_certs'
default_template = "about.html"
exception_template = 'empty_dynamic_content.html'

since_date = {'pl': 'Od', 'en': 'Since'}
position = {'pl':'Stanowisko','en':'Position'}
to_date = {'pl': 'Do', 'en': 'To'}


class MenuItem():
    template = None
    url_page_path = None
    description = {}
    
    def __init__(self, template, url_page_path=exception_template,  description={}):
        self.template = template
        self.url_page_path = url_page_path
        self.description = description
        
    def getDescription(self, current_language):
        if isLanguageSupported(current_language):
            return self.description.get(current_language)
        return self.description.get(default_language)
        

menu = [MenuItem(url_page_path='about', template="about.html", description={"pl":"O mnie", "en":"About myself"}),
        MenuItem(url_page_path='employment', template="employment.html", description={"pl":"Zatrudnienie", "en":"Employment"}),
             MenuItem(url_page_path='education', template="education.html", description={"pl":"Edukacja", "en":"Education"}),
             MenuItem(url_page_path='experience', template="experience.html", description={"pl":u"Doświadczenie", "en":"Experience"})
             ]

experience = [MenuItem(url_page_path='ajax_certs',template="experience_certs.html"),
              MenuItem(url_page_path='ajax_skills', template="experience_skills.html"),
              MenuItem(url_page_path='ajax_projects', template="experience_projects.html")]



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
        self.redirect('/cv')

   

class BusinessCard(webapp.RequestHandler):
    ''' Handler for standard synchronous HTTP request'''
    
    def get(self):
        '''URL context path knows about application state:
            * first position is a application contxt entry
            * current language is at second position   
            * third position contains name for page controller that is obligated to return data
            So there is need to parse URL path and split it content to array elements  
        '''
        splitted_url_path = splitURLPath(self.request.path)        
        language = currentLanguage(splitted_url_path)
        controller_name = currentController(splitted_url_path)
        logging.info("Template lookup for: " + controller_name)
        template_values = self.resolveModel(language, controller_name)
        self.response.out.write(self.templateResolve(controller_name).render(template_values))

    def resolveModel(self, language, controller_name):
        content = self.resolveContent(controller_name)
        title = {'pl': u'Trochę informacji o mnie', 'en': 'Some info about me'}
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
            if item.url_page_path == controller_name:           
                template = jinja_environment.get_template(item.template)
                break
        return template

class CVRPCHandler(webapp.RequestHandler):
    
    """ Will handle the RPC requests."""
    def get(self):        
        logging.info(self.request.path)
        splitted_url_path = splitURLPath(self.request.path)        
        language = currentLanguage(splitted_url_path)
        controller_name = currentAjaxController(splitted_url_path)
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
        template = jinja_environment.get_template(exception_template)
        for item in experience:
            if item.url_page_path == controller_name:           
                template = jinja_environment.get_template(item.template)
                break
        return template
    
application = webapp.WSGIApplication([('/', Main), (r'/cv.*/ajax.*', CVRPCHandler), (r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
