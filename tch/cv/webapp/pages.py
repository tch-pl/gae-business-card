#-*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2

"""Author: Tomasz Chrul"""

#TODO
"""fix encoding (to support polish characters)"""


template_path = 'tch/cv/webapp/web/'
default_language = 'pl'
supported_languages = ['pl', 'en']
default_controller = 'employment'

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
        

menu = [MenuItem('employment', "employment.html", {"pl":"Zatrudnienie", "en":"Employment"}), 
             MenuItem('education', "index.html", {"pl":"Edukacja", "en":"Education"}), 
             MenuItem('experience', "index.html", {"pl":"Doswiadczenie", "en":"Experience"}), 
             MenuItem('about', "index.html", {"pl":"O mnie", "en":"About myself"})]


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
        title = {'pl': 'Troche informacji o mnie','en': 'Some info about me'}
        model = {
                 'menu' : menu,
                 'language' : language,
                 'title' : title,
                 'supported_languages' : supported_languages,
                 'content' : content                 
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
        if controller_name == 'employment':
            return {"employment" : EmploymentHistory()}
        elif 'education' == controller_name:
            return {"education" : Education}
        elif 'experience' == controller_name:
            return {"education" : Education}
        elif 'about' == controller_name:
            return {"education" : Education}
        else:
            return {"employment" : EmploymentHistory()}

class EmploymentHistory():            
    def __init__(self,user=""):
        self.history = [Employment("Optix Sp. z o. o.", 
                                   '2006-09', '2007-11', 
                                   {'pl':'Programista', 'en':'Software Developer'}, 
                                   {'pl':'', 'en':''}),
                   Employment("BLStream Sp. z o. o.", 
                              '2007-12', '2010-06', 
                              {'pl':'Programista', 'en':'Software Developer'}, 
                              {'pl':'', 'en':''}),
                   Employment("BLStream Sp. z o. o.", 
                              '20010-07', '2011-05', 
                              {'pl':'Starszy Programista', 
                               'en':'Senior Software Developer'}, 
                              {'pl':['Utrzymanie i rozwoj aplikacji typu selfcare', 'Tworzenie dokumentacji technicznej'], 
                               'en':['Maintenance and development of selfcare web application', 'Writing technical documentation' ]}),
                   Employment("BLStream Sp. z o. o.", 
                              '20011-06', '2013-04', 
                              {'pl':'Techniczny Lider Projektu', 'en':'Technical Project Leader'}, 
                              {'pl':
                                    ['Koordynacja pracy zespolu projektowego', 'Komunikacja z klientem', 'Wsparcie techniczne zespolu i klienta'], 
                                'en':['development team coordination', 'communication with customer', 'technical support for team and customer']})
                   ]
        

class Employment():    
    def __init__(self,company, start_date, end_date, position, description):
        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.position = position
        self.description = description


    

class Education():
    pass

    
application = webapp.WSGIApplication([('/',Main),(r'/cv.*', BusinessCard)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

