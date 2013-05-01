'''
Created on May 1, 2013

@author: Baptiste Maingret

Classes defining the Entity stored in the AppEngine Datastore
'''
from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()
    name = db.StringProperty()

class Service(db.Model):
    name = db.StringProperty(required=True)
    
class UserService(db.Model):
    user_id = db.ReferenceProperty(User,
                                   required=True,
                                   collection_name='user_services')
    service_id = db.ReferenceProperty(Service,
                                      required=True)
    access_token = db.StringProperty(required=True)
    refresh_token = db.StringProperty(required=True)

class LocalServer(db.Model):
    authentication_token = db.StringProperty(required=True)
    
class Task(db.Model):
    user_service_id = db.Reference(UserService,
                                   required=True,
                                   collection_name='tasks')
    local_server_id = db.ReferenceProperty(LocalServer,
                                           required=True,
                                           collection_name='tasks')
    creation_date = db.DateTimeProperty(auto_now_add=True,
                                        required=True)
    completion_date = db.DateTimeProperty(required=True)
    number_of_files = db.IntegerProperty(required=True)
    status = db.StringProperty(required=True,
                               choices=('created', 'validated', 'in_progress', 'done'))