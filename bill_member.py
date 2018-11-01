from datetime import datetime
from load_readings import get_readings
from tariff import BULB_TARIFF


def calculate_dayly_cost_for_tariff(utility_type='electricity', date=None):
    """
    Calculates standard daily accuring price
    :param utility_type: electricity or gas
    :param date: e.g. '2017-05-29'
    :return: accrued cost for the day in penc
    """
    util_types = ('electricity', 'gas')

    if utility_type not in util_types:
        raise ValueError('Incorrect utility type')

    if not date:
        raise ValueError('Date needs to be provided')

    # TODO create a Decimal Type with 2 digit precision
    days = float(date.split('-')[-1])

    if days > 31 or days < 0:
        raise ValueError("Month days can't be bigger then 31 or negative")

    dayly_amount = BULB_TARIFF.get(utility_type).get('standing_charge')

    return days * dayly_amount



def calculate_total_amount_and_kwh_usage(information, utility_type='electricity', date=None):
    """
     Update the Reading Structure with the consumtion for the month
    :param information: list
    :return: updated_list
    """
    util_types = ('electricity', 'gas')

    if utility_type not in util_types:
        raise ValueError('Incorrect utility type')

    if not date:
        raise ValueError('Date needs to be provided')

    today = datetime.now()
    date_input = datetime.strptime(date, '%Y-%m-%d')

    if today < date_input:
        raise ValueError('Date is in the future')


    tariff = BULB_TARIFF.get(utility_type).get('unit_rate')
    amount = calculate_dayly_cost_for_tariff(utility_type=utility_type, date=date)
    kwh = 0
    for i, bill in enumerate(information):
        # Exclude first month kwh calculation
        if i is not 0:
            if date in information[i].get('readingDate'):
                kwh = information[i].get('cumulative') \
                            - information[i - 1].get('cumulative')

                amount = kwh * tariff + amount
    # convert amount to pounds
    # TODO to avoid floating point errors us Decimal type
    amount = round((amount / 100), 2)
    return amount, kwh


def calculate_bill(member_id=None, account_id=None, bill_date=None,  utility_type='electricity'):
    """
    Returns the amount and kwh
    :param member_id:
    :param account_id:
    :param bill_date:
    :param utility_type:
    :return:
    """

    member_information = get_readings().get(member_id) or None

    if member_information is not None:
        # Retrieve Account Information
        if account_id == 'ALL':
            account_id = list(member_information[0].keys())[0]

        account_information = member_information[0].get(account_id) or None
        if account_information is not None:
            # TODO get all account ids
            # Check for electricity
            electricy_information = account_information[0].get(utility_type) or None

            if electricy_information is not None:
                # Update the Reading Structure with the consumtion for the month
                amount, kwh = calculate_total_amount_and_kwh_usage(electricy_information,
                                                                             utility_type=utility_type,
                                                                             date=bill_date)

                return amount, kwh

    amount = 0
    kwh = 0
    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
