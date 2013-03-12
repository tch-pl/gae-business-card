from google.appengine.ext import db
from google.appengine.ext.db import polymodel
    
class ContactData(polymodel.PolyModel):
    phone_number = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
    email = db.EmailProperty()
    
    
class PersonalData(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
