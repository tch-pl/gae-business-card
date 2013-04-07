'''
Created on 07-04-2013

@author: tch
'''

import json

class CVContentFactory():
    def generateContent(self, controller_name, user=""):
        historyContent = HistoryContent()        
        if 'employment' == controller_name:
            return {"employment" : historyContent.employmentHistory}
        elif 'education' == controller_name:
            return {"education" : historyContent.educationHistory}
        elif 'experience' == controller_name:
            return {"experience" : historyContent.experience_categories}
        elif 'about' == controller_name:
            return {"employment" : historyContent.educationHistory}
        else:
            return {"employment" : historyContent.employmentHistory}

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
        self.experience_categories = json.load(open('data/experience_categories.json', 'r'))
        
