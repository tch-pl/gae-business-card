'''
Created on 16-02-2013

@author: user
'''
from tch.cv.model.ext.Person import ContactData, PersonalData
from tch.cv.model.ext.CV import Company, CV, Experience, position_categories

from datetime import date

def createCV(uId):
    cv = CV()
    cv.contact_data = createContactData()
    cv.personal_data = createPersonalData()
    cv.experience = createExperience()
    return cv

def createContactData():
    contactData = ContactData()
    contactData.address = "Slupsk"
    contactData.email = "abc.aaa@fff"
    contactData.phone_number = "+48777888999"
    return contactData

def createPersonalData():
    data = PersonalData()
    data.first_name = "first name"
    data.last_name = "last_name"
    return data


def createExperience():
    experiences = []
    exp = Experience()
    exp.company = "BLStream"
    exp.start_date = date(2008, 12, 3)
    exp.end_date = date(2013, 4, 30)
    exp.position = position_categories.index(1)
    experiences.append(exp)
    
    return experiences

def createCompany(name):
    company = Company()
    company.name=name
    return company


if __name__ == '__main__':
    print createCV('')