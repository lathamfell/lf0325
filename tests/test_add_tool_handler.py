import unittest
from handlers.add_tool_handler import AddToolHandler
import os

class TestAddToolHandler(unittest.TestCase):

    def test_add_tool_handler_no_existing_tool(self):
        os.remove('tinydb_test.json')
        test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_json = {
            'type': 'Ladder',
            'code': 'LADW',
            'brand': 'DeWalt'
        }
        result = test_handler.handle(test_json)
        self.assertEqual(result, "Tool LADW inserted")

    def test_add_tool_handler_existing_tool(self):
        os.remove('tinydb_test.json')
        test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_json = {
            'type': 'Ladder',
            'code': 'LADW',
            'brand': 'DeWalt'
        }
        test_handler.handle(test_json)
        # duplicate insert
        result = test_handler.handle(test_json)
        self.assertEqual('409 CONFLICT', result.status)
