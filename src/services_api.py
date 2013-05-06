'''
Created on May 4, 2013

@author: Baptiste Maingret
'''

from google.appengine.ext import endpoints

import local_server_api


application = endpoints.api_server([local_server_api.LocalServerAPI],
                                    restricted=False)
