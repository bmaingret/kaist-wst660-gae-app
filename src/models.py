'''
Created on May 1, 2013

@author: Baptiste Maingret

Classes defining the Entity stored in the AppEngine Datastore
'''
from google.appengine.ext import db

class BaseModel(db.Model):
    _ref_properties = dict()
    
    def to_message(self, *args, **kwargs):
        model_class_name = self.__class__.__name__
        message_class_name = ''.join((model_class_name, 'Message'))
        messages_module = __import__(kwargs.pop('import_module', 'api_messages'))
        message_class = getattr(messages_module, message_class_name)
        attributes = {attr: getattr(self, attr) for attr in args}
        return message_class(**attributes)
    
    @classmethod
    def from_message(cls, message, *args):
        attributes = {attr: getattr(message, attr) for attr in args}
        for attribute, property in cls._ref_properties.items():
            attributes[attribute] = db.Key(encoded=getattr(message, property))
        entity = cls(**attributes)     
        return entity
    
    @classmethod
    def put_from_message(cls, message, *args):
        entity = cls.from_message(message, *args)
        entity.put()
    
    @staticmethod
    def _get_attr_id_builder(attribute_name):
        def _get_attr_id(self):
            return str(getattr(self, attribute_name).key())
        return _get_attr_id
    
    @staticmethod
    def _set_attr_id_builder(attribute_name):
        def _set_attr_id(self, id):
            setattr(self, attribute_name, db.Key(encoded=id))
        return _set_attr_id
    

            
    
class User(BaseModel):
    email = db.EmailProperty()
    name = db.StringProperty()

class Service(BaseModel):
    name = db.StringProperty(required=True)
    
class UserService(BaseModel):
    user = db.ReferenceProperty(User,
                                   required=True,
                                   collection_name='user_services')
    service = db.ReferenceProperty(Service,
                                      required=True)
    access_token = db.StringProperty(required=True)
    refresh_token = db.StringProperty(required=True)
    user_id = property(BaseModel._get_attr_id_builder('user'))
    service_id = property(BaseModel._get_attr_id_builder('service'))


class LocalServer(BaseModel):
    authentication_token = db.StringProperty(required=True)
    
class Task(BaseModel):
    user_service = db.Reference(UserService,
                                   required=True,
                                   collection_name='tasks')
    local_server = db.ReferenceProperty(LocalServer,
                                           required=True,
                                           collection_name='tasks')
    creation_date = db.DateTimeProperty(auto_now_add=True,
                                        required=True)
    completion_date = db.DateTimeProperty()
    number_of_files = db.IntegerProperty(required=True)
    status = db.StringProperty(required=True,
                               choices=set(['created', 'validated', 'in_progress', 'done']))
    user_service_id = property(BaseModel._get_attr_id_builder('user_service'))
    local_server_id = property(BaseModel._get_attr_id_builder('local_server'))
    
    