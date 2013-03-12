from google.appengine.ext import db
from tch.cv.model.ext.Person import PersonalData, ContactData


position_categories = ('developer', 'PM', 'analyst')

class Company(db.Model):
    name = db.StringProperty(required=True)
    
class Experience(db.Model):
    start_date = db.DateProperty()
    end_date = db.DateProperty()
    company = db.ReferenceProperty(Company)
    position = db.StringProperty(required=True,
                           choices=set(position_categories))

class CV(db.Model):
    personal_data = db.ReferenceProperty(PersonalData)
    contact_data = db.ReferenceProperty(ContactData)
    experience = db.ReferenceProperty(Experience, collection_name='experience')