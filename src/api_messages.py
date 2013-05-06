'''
Created on May 4, 2013

@author: Baptiste Maingret
'''

from protorpc import messages
from protorpc.message_types import DateTimeField

class TaskRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a task query"""
    task_id = messages.IntegerField(1, required=True)
    
class TaskMessage(messages.Message):
    """ProtoRPC message definition to represent a task"""
    user_service_id = messages.StringField(1)
    local_server_id = messages.StringField(2)
    creation_date = DateTimeField(3)
    completion_date = DateTimeField(4)
    number_of_files = messages.IntegerField(5)
    status = messages.StringField(6)
    
class UserServiceMessage(messages.Message):
    """ProtoRPC message definition to represent a service for which the user has provided authorization"""
    user_id = messages.StringField(1)
    service_id = messages.StringField(2)
    access_token = messages.StringField(3)
    refresh_token = messages.StringField(4)
    service_name = messages.StringField(5)
    
class TasksMessage(messages.Message):
    """ProtoRPC message definition to represent a list of tasks"""
    tasks = messages.MessageField(TaskMessage, 1)
    
class UserServicesMessage(messages.Message):
    """ProtoRPC message definition to represent a list of tasks"""
    user_services = messages.MessageField(UserServiceMessage, 1)

