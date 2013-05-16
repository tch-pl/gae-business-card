'''
Created on 07-04-2013

@author: tch
'''

import json

class CVContentFactory():
    
    epmloyment = 'employment'
    education = 'education'
    experience = 'experience'
    about = 'about'
    
    def generateEmployment(self):
        return self.generateContent(self.employment)
    
    def generateEducation(self):
        return self.generateContent(self.education)
    
    def generateExperience(self):
        return self.generateContent(self.experience)
    
    def generateAbout(self):
        return self.generateContent(self.about)
    
    def generateContent(self, controller_name, user=""):
        historyContent = HistoryContent()
        if self.epmloyment == controller_name:
            return {self.epmloyment : historyContent.employmentHistory}
        elif self.education == controller_name:
            return {self.education : historyContent.educationHistory}
        elif self.experience == controller_name:
            return {self.experience : historyContent.experience_categories}
        elif self.about == controller_name:
            return {self.about : None}
        else:
            return {"employment" : historyContent.employmentHistory}


class CVExperienceContentFactory():
    def generateContent(self, controller_name, user=""):
        experience = Experience()
        if 'ajax_certs' == controller_name:
            return {"certs" : experience.certs}
        elif 'ajax_projects' == controller_name:
            return {"projects" : experience.projects}
        elif 'ajax_skills' == controller_name:
            return {"skills" : experience.skills}
        else:
            return {"certs" : experience.certs}


class HistoryContent():            
    def __init__(self, user=""):
        self.employmentHistory = json.load(open('data/employment.json', 'r')) 
        self.educationHistory = json.load(open('data/education.json', 'r'))
        self.experience_categories = json.load(open('data/experience_categories.json', 'r'))
        

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
        
class Experience():
    def __init__(self, user=""):
        self.certs = json.load(open('data/experience_certs.json', 'r'))
        self.projects = json.load(open('data/experience_projects.json', 'r'))
        self.skills = json.load(open('data/experience_skills.json', 'r'))
        
