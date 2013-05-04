'''
Created on May 4, 2013

@author: Baptiste Maingret
'''
import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from protorpc import messages
import models


class TestModel(models.BaseModel):
    test_string = db.StringProperty(required=True)
    test_int = db.IntegerProperty()
    test_bool = db.BooleanProperty()
    
class TestModelMessage(messages.Message):
    test_string = messages.StringField(1)
    test_int = messages.IntegerField(2)
    test_bool= messages.BooleanField(3)
        
class Test(unittest.TestCase):
    """ Test class for the model module"""
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        
        self.entity = TestModel(test_string="test string", test_int=2)

    def tearDown(self):
        self.testbed.deactivate()

    def test_to_message(self):
        empty_message = self.entity.to_message(import_module='test_models')
        message = self.entity.to_message('test_string', 'test_int',
                                         import_module='test_models')
        self.assertIsInstance(message, TestModelMessage)
        self.assertIsNone(empty_message.test_string)
        self.assertIsNone(message.test_bool)
        self.assertIs(message.test_string, self.entity.test_string)
        self.assertIs(message.test_int, self.entity.test_int)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_to_message']
    unittest.main()