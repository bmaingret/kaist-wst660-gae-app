'''
Created on May 4, 2013

@author: Baptiste Maingret
'''
import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from protorpc import messages
import models

class TestModel2(models.BaseModel):
    test_string = db.StringProperty(required=True)

class TestModel(models.BaseModel):
    _ref_properties = {'test2': 'test_id'}
    test_string = db.StringProperty(required=True)
    test_int = db.IntegerProperty()
    test_bool = db.BooleanProperty()
    test2 = db.ReferenceProperty(TestModel2)
    test_id = property(models.BaseModel._get_attr_id_builder('test2'),
                       models.BaseModel._set_attr_id_builder('test2'))
    
class TestModelMessage(messages.Message):
    test_string = messages.StringField(1)
    test_int = messages.IntegerField(2)
    test_bool = messages.BooleanField(3)
    test_id = messages.StringField(4)
        
class Test(unittest.TestCase):
    """ Test class for the model module"""
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.entity2 = TestModel2(test_string="test entity 2 ")
        self.entity2.put()
        self.entity = TestModel(test_string="test string",
                                test_int=2,
                                test2 = self.entity2)
        self.empty_message = self.entity.to_message(import_module='test_models')
        self.message = self.entity.to_message('test_string', 'test_int', 'test_id',
                                         import_module='test_models')

    def tearDown(self):
        self.testbed.deactivate()

    def test_to_message(self):
        self.assertIsInstance(self.message, TestModelMessage)
        self.assertIsNone(self.empty_message.test_string)
        self.assertIsNone(self.message.test_bool)
        self.assertIs(self.message.test_string, self.entity.test_string)
        self.assertIs(self.message.test_int, self.entity.test_int)
    
    def test_get_attr_id(self):
        self.assertIs(self.entity.test_id, str(self.entity.test2.key()))
        self.assertIs(self.message.test_id, self.entity.test_id)
        self.assertIs(self.message.test_id, str(self.entity.test2.key()))  
  
    def test_set_attr_id(self):
        self.test_entity = TestModel2(test_string="test")
        self.test_entity.put()
        self.entity.test_id = str(self.test_entity.key())
        self.assertEqual(self.entity.test2.test_string, self.test_entity.test_string)
          
    def test_from_message(self):
        from_message = TestModel.from_message(self.message, *('test_string',
                                                             'test_int',
                                                             'test_id')) 
        self.assertIs(self.entity.test_string, from_message.test_string)
        self.assertIs(self.entity.test_int, from_message.test_int)
        self.assertEqual(self.entity.test_id, from_message.test_id)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_to_message']
    unittest.main()