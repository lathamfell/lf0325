import unittest
from handlers.add_tool_handler import AddToolHandler
from handlers.update_tool_handler import UpdateToolHandler
from tests.helpers import silent_remove

class TestAddToolHandler(unittest.TestCase):

    def test_update_tool_handler_no_existing_tool(self):
        # setup
        silent_remove('tinydb_test.json')
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Ladder',
            'code': 'LADW',
            'brand': 'DeWalt'
        }
        add_test_handler.handle(test_add_json)
        # test
        update_tool_handler = UpdateToolHandler(db_path='tinydb_test.json')
        test_update_json = {
            'type': 'Chainsaw',
            'daily_charge': '2.99',
            'weekend_charge': True,
            'weekday_charge': False,
            'holiday_charge': True
        }
        result = update_tool_handler.handle(test_update_json)

        self.assertEqual('404 NOT FOUND', result.status)

        # teardown
        silent_remove('tinydb_test.json')

    def test_update_tool_handler_existing_tool(self):
        # setup
        silent_remove('tinydb_test.json')
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Ladder',
            'code': 'LADW',
            'brand': 'DeWalt'
        }
        add_test_handler.handle(test_add_json)
        # test
        update_tool_handler = UpdateToolHandler(db_path='tinydb_test.json')
        test_update_json = {
            'type': 'Ladder',
            'daily_charge': '2.99',
            'weekend_charge': True,
            'weekday_charge': False,
            'holiday_charge': True
        }
        result = update_tool_handler.handle(test_update_json)

        self.assertEqual('Tool updated', result)

        # teardown

        silent_remove('tinydb_test.json')
