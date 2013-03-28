#-*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import json

"""Author: Tomasz Chrul"""

#TODO
"""

"""


template_path = 'tch/cv/webapp/web/'
default_language = 'pl'
supported_languages = ['pl', 'en']
default_controller = 'about'

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
             MenuItem('experience', "index.html", {"pl":u"Doświadczenie", "en":"Experience"})
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
    
    if len(splitted_path) > 2:
        return [splitted_path[0], splitted_path[1], splitted_path[2]]        
    elif len(splitted_path) > 1:
        return [splitted_path[0], splitted_path[1]]
    
def isLanguageSupported(language):
    for lang in supported_languages:
        if lang == language:
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
        controlled_content = CVContentFactory().generateContent(controller_name)
        main_content = {"profession": "Software Engineer",
                 "full_name" : "Tomasz Chrul"}
        
        content = main_content.copy()
        content.update(controlled_content)                                        
        return content


class CVContentFactory():
    def generateContent(self, controller_name, user=""):
        historyContent = HistoryContent()        
        if 'employment' == controller_name:
            return {"employment" : historyContent.employmentHistory}
        elif 'education' == controller_name:
            return {"education" : historyContent.educationHistory}
        elif 'experience' == controller_name:
            return {"education" : historyContent.educationHistory}
        elif 'about' == controller_name:
            return {"education" : historyContent.educationHistory}
        else:
            return {"employment" : historyContent.employmentHistory}

class HistoryContent():            
    def __init__(self, user=""):
        self.employmentHistory = json.load(open('data/employment.json', 'r')) 
        self.educationHistory = json.load(open('data/education.json', 'r')) 
 

class History():
    def __init__(self, start_date, end_date, description):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description


class Employment(History):    
    def __init__(self, company, start_date, end_date, position, description):
        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.position = position
        self.description = description

class Education(History):
    def __init__(self, school, start_date, end_date, degree, description, additional_data):
        self.school = school
        self.start_date = start_date
        self.end_date = end_date        
        self.description = description
        self.degree = degree
        self.additional_data = additional_data

    
application = webapp.WSGIApplication([('/', Main), (r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
   HistoryContent()
