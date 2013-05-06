'''
Created on May 4, 2013

@author: Baptiste Maingret
'''
import datetime
from protorpc import remote

from google.appengine.ext import endpoints

from models import Task, UserService, User, Service, LocalServer
from api_messages import TaskRequestMessage, TaskMessage

@endpoints.api(name='localserver', version='v1',
               description='Local Server API')
class LocalServerAPI(remote.Service):
    '''Class that defines the Local Server API endpoints'''

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
        user = User()
        user.put()
        service = Service(name = "service name")
        service.put()
        ls = LocalServer(authentication_token = "auth token")
        ls.put()
        us = UserService(user_id=user.key(),
                         service_id=service.key(),
                         access_token="access token",
                         refresh_token="refresh token")
        us.put()
        message = Task(user_service_id=us,
                    local_server_id=ls.key(),
                    completion_date = datetime.datetime(2013,01,01,00,00),
                    number_of_files=1,
                    status='created').to_message()
        message = TaskMessage(user_service_id="qw")
        return message
    
    def get_tasks(self, request):
        pass



        