import datetime
import unittest
from load_readings import get_readings
from bill_member import (calculate_dayly_cost_for_tariff,
                         calculate_total_amount_and_kwh_usage
                         )

from bill_member import calculate_bill


class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


    def test_calculate_dayly_cost_for_tariff(self):
        month = '2017-08-31'
        price = 24.56
        days = 31
        test_amount = days * price
        amount = calculate_dayly_cost_for_tariff(utility_type='electricity', date=month)
        self.assertEqual(amount, test_amount)

    def test_calculate_dayly_cost_for_tarif_wrong_date_input(self):
        month = '2017-08-35'

        with self.assertRaises(Exception) as context:
            amount = calculate_dayly_cost_for_tariff(utility_type='electricity', date=month)
        self.assertIn("Month days can't be bigger then 31 or negative", str(context.exception))

        month = None

        with self.assertRaises(Exception) as context:
            amount = calculate_dayly_cost_for_tariff(utility_type='electricity', date=month)
        self.assertIn("Date needs to be provided", str(context.exception))

    def test_calculate_dayly_cost_for_tarif_wrong_utility_type(self):
        month = '2017-08-35'
        utility='test'

        with self.assertRaises(Exception) as context:
            amount = calculate_dayly_cost_for_tariff(utility_type=utility, date=month)
        self.assertIn("Incorrect utility type", str(context.exception))


    def test_calculate_total_amount_and_kwh_usage(self):
        month = '2017-08-31'
        member_id = 'member-123'
        account_id = 'account-abc'
        test_amount = 27.57
        test_kwh = 167
        member_information = get_readings().get(member_id)
        account_information = member_information[0].get(account_id)
        electricy_information = account_information[0].get('electricity')

        amount, kwh = calculate_total_amount_and_kwh_usage(electricy_information,
                                                           utility_type='electricity',
                                                           date=month)

        self.assertEqual(amount, test_amount)
        self.assertEqual(kwh, test_kwh)

    def test_calculate_total_amount_and_kwh_usage_wrong_date_in_the_future(self):
        month = '2019-08-31'
        member_id = 'member-123'
        account_id = 'account-abc'
        member_information = get_readings().get(member_id)
        account_information = member_information[0].get(account_id)
        electricy_information = account_information[0].get('electricity')

        with self.assertRaises(Exception) as context:
            amount, kwh = calculate_total_amount_and_kwh_usage(electricy_information,
                                                               utility_type='electricity',
                                                               date=month)

        self.assertIn("Date is in the future", str(context.exception))

    def test_calculate_total_amount_and_kwh_usage_no_date_provided(self):
        month = None
        member_id = 'member-123'
        account_id = 'account-abc'
        member_information = get_readings().get(member_id)
        account_information = member_information[0].get(account_id)
        electricy_information = account_information[0].get('electricity')

        with self.assertRaises(Exception) as context:
            amount, kwh = calculate_total_amount_and_kwh_usage(electricy_information,
                                                               utility_type='electricity',
                                                               date=month)

        self.assertIn("Date needs to be provided", str(context.exception))

    def test_calculate_total_amount_and_kwh_usage_incorrect_utility(self):
        month = '2017-08-31'
        member_id = 'member-123'
        account_id = 'account-abc'
        member_information = get_readings().get(member_id)
        account_information = member_information[0].get(account_id)
        electricy_information = account_information[0].get('electricity')

        with self.assertRaises(Exception) as context:
            amount, kwh = calculate_total_amount_and_kwh_usage(electricy_information,
                                                               utility_type='tests',
                                                               date=month)

        self.assertIn("Incorrect utility type", str(context.exception))




if __name__ == '__main__':
    unittest.main()
