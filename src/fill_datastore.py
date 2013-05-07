'''
Created on May 7, 2013

@author: Baptiste Maingret
'''

from google.appengine.ext import db
from models import *

def fill():
    ls = LocalServer(authentication_token="ls auth")
    ls.put()
    
    s = Service(name="service name")
    s.put()
    
    u = User(name="username", email="user email")
    u.put()
    
    us = UserService(user=u,
                     service=s,
                     access_token="us access token",
                     refresh_token="us refresh token")
    us.put()
    
    t = Task(user_service=us,
             local_server=ls,
             number_of_files=1,
             status='created',
             )
    t.put()
    t2 = Task(user_service=us,
             local_server=ls,
             number_of_files=2,
             status='created',
             )
    t2.put()