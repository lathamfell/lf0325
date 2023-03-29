import unittest
from handlers.transaction_handler import TransactionHandler
from handlers.add_tool_handler import AddToolHandler
from tests.helpers import silent_remove

from handlers.update_tool_handler import UpdateToolHandler


class TestTransactionHandler(unittest.TestCase):

    def test_transaction_handler_discount_percent_too_high(self):
        # setup
        silent_remove('tinydb_test.json')
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Jackhammer',
            'code': 'JAKR',
            'brand': 'DeWalt'
        }
        add_test_handler.handle(test_add_json)
        # test
        transaction_handler = TransactionHandler(
            {
              "rental_day_count": '5',
              "discount_percent": '101',
              'tool_code': 'JAKR',
              'check_out_date': '2015-09-03'
            },
            db_path="tinydb_test.json")
        self.assertRaises(
            ValueError, transaction_handler.handle
        )

        # teardown
        silent_remove('tinydb_test.json')

    def test_transaction_handler_fourth_of_july_on_weekend(self):
        # setup
        silent_remove('tinydb_test.json')
        # add ladder tool
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Ladder',
            'code': 'LADW',
            'brand': 'Little Giant'
        }
        add_test_handler.handle(test_add_json)

        # update ladder tool
        update_tool_handler = UpdateToolHandler(db_path='tinydb_test.json')
        test_update_json = {
            'type': 'Ladder',
            'daily_charge': '2.99',
            'weekend_charge': True,
            'weekday_charge': True,
            'holiday_charge': False
        }
        update_tool_handler.handle(test_update_json)

        # test
        transaction_handler = TransactionHandler(
            {
                "rental_day_count": '3',
                "discount_percent": '10',
                'tool_code': 'LADW',
                'check_out_date': '2020-07-02'
            },
            db_path="tinydb_test.json")
        result = transaction_handler.handle()

        expected_result = {
            'charge_days': 2,
            'check_out_date': '07/02/20',
            'daily_charge': '$2.99',
            'discount_amount': '$0.60',
            'discount_percent': '10%',
            'due_date': '07/05/20',
            'final_charge': '$5.38',
            'pre_discount_charge': '$5.98',
            'rental_day_count': 3,
            'tool_brand': 'Little Giant',
            'tool_code': 'LADW',
            'tool_type': 'Ladder'
        }

        self.assertEqual(expected_result, result)

        # teardown
        silent_remove('tinydb_test.json')


    def test_transaction_handler_fourth_of_july_on_weekend_no_weekend_charge(self):
        # setup
        silent_remove('tinydb_test.json')
        # add ladder tool
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Chainsaw',
            'code': 'CHNS',
            'brand': 'Stihl'
        }
        add_test_handler.handle(test_add_json)

        # update chainsaw tool
        update_tool_handler = UpdateToolHandler(db_path='tinydb_test.json')
        test_update_json = {
            'type': 'Chainsaw',
            'daily_charge': '1.49',
            'weekend_charge': False,
            'weekday_charge': True,
            'holiday_charge': True
        }
        update_tool_handler.handle(test_update_json)

        # test
        transaction_handler = TransactionHandler(
            {
                "rental_day_count": '5',
                "discount_percent": '25',
                'tool_code': 'CHNS',
                'check_out_date': '2015-07-02'
            },
            db_path="tinydb_test.json")
        result = transaction_handler.handle()

        expected_result = {
            'charge_days': 3,
            'check_out_date': '07/02/15',
            'daily_charge': '$1.49',
            'discount_amount': '$1.12',
            'discount_percent': '25%',
            'due_date': '07/07/15',
            'final_charge': '$3.35',
            'pre_discount_charge': '$4.47',
            'rental_day_count': 5,
            'tool_brand': 'Stihl',
            'tool_code': 'CHNS',
            'tool_type': 'Chainsaw'
        }

        self.assertEqual(expected_result, result)

        # teardown
        silent_remove('tinydb_test.json')


    def test_transaction_handler_labor_day(self):
        # setup
        silent_remove('tinydb_test.json')
        # add ladder tool
        add_test_handler = AddToolHandler(db_path='tinydb_test.json')
        test_add_json = {
            'type': 'Jackhammer',
            'code': 'JAKD',
            'brand': 'DeWalt'
        }
        add_test_handler.handle(test_add_json)

        # update chainsaw tool
        update_tool_handler = UpdateToolHandler(db_path='tinydb_test.json')
        test_update_json = {
            'type': 'Jackhammer',
            'daily_charge': '2.99',
            'weekend_charge': False,
            'weekday_charge': True,
            'holiday_charge': False
        }
        update_tool_handler.handle(test_update_json)

        # test
        transaction_handler = TransactionHandler(
            {
                "rental_day_count": '6',
                "discount_percent": '0',
                'tool_code': 'JAKD',
                'check_out_date': '2015-09-03'
            },
            db_path="tinydb_test.json")
        result = transaction_handler.handle()

        expected_result = {
            'charge_days': 3,
            'check_out_date': '09/03/15',
            'daily_charge': '$2.99',
            'discount_amount': '$0.00',
            'discount_percent': '0%',
            'due_date': '09/09/15',
            'final_charge': '$8.97',
            'pre_discount_charge': '$8.97',
            'rental_day_count': 6,
            'tool_brand': 'DeWalt',
            'tool_code': 'JAKD',
            'tool_type': 'Jackhammer'
        }

        self.assertEqual(expected_result, result)

        # teardown
        silent_remove('tinydb_test.json')
