'''
Created on May 4, 2013

@author: Baptiste Maingret
'''
import datetime
from protorpc import remote, message_types

from google.appengine.ext import endpoints

from models import Task, UserService, User, Service, LocalServer
from api_messages import *
from google.appengine.ext.endpoints.api_exceptions import NotFoundException,\
    ForbiddenException
import fill_datastore

@endpoints.api(name='localserver', version='v1',
               description='Local Server API')
class LocalServerAPI(remote.Service):
    '''Class that defines the Local Server API endpoints'''
    
    def __init__(self):
        #fill_datastore.fill()
        pass
    
    @endpoints.method(TaskRequestMessage, TaskMessage,
                      path='task', http_method='GET',
                      name='ls.gettask')    
    def get_task(self, request):
        """Exposes an API endpoint to retrieve a specific task from its ID.

        Args:
            request: An instance of TaskMessage parsed from the API request.

        Returns:
            An instance of TaskMessage corresponding to ID supplied
        """        
        query = Task.all()
        query.filter('__key__ =', request.task_id)
        task = query.get()
        if task is None:
            raise NotFoundException()
        task_message = task.to_message(*LocalServerFields.Task)
        return task_message
    
    @endpoints.method(TaskMessage,
                      path='task', http_method='POST',
                      name='ls.addtask')       
    def add_task(self, request):
        query = LocalServer.all(keys_only=True)
        query.filter('authentication_token =', request.auth_token)
        local_server = query.get()
        if local_server is None:
            raise ForbiddenException
        Task.put_from_message(request)
        return message_types.VoidMessage()
        

    @endpoints.method(TasksRequestMessage, TasksMessage,
                      path='tasks', http_method='GET',
                      name='ls.gettasks')      
    def get_tasks(self, request):
        print ''.join(["gettasks: ", request.auth_token])
        query = LocalServer.all()
        query.filter('authentication_token =', request.auth_token)
        local_server = query.get()
        if local_server is None:
            raise ForbiddenException()
        tasks = [task.to_message(*LocalServerFields.Task) for task in local_server.tasks]
        return TasksMessage(tasks=tasks)
    
    @endpoints.method(UserMessage,
                      path='user', http_method='POST',
                      name='ls.adduser')  
    def add_user(self, request):
        query = LocalServer.all(keys_only=True)
        query.filter('authentication_token =', request.auth_token)
        local_server = query.get()
        if local_server is None:
            raise ForbiddenException
        User.put_from_message(request, 'email', 'name')
        return message_types.VoidMessage()        
        



        