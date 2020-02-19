# --------------------------------------------------------------
# RETURNS THE MENU OF THE APPROPRIATE ITEM FROM THE VENUES TABLE
# GIVEN THE VENUE ID AND TYPE ID

# LAST EDITED: 7.02.2020
# --------------------------------------------------------------

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# RPC protocol required for Odoo
import xmlrpc.client


class DecimalEncoder(json.JSONEncoder):
    """Format JSON decimals appropriately"""

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Credentials')

    try:
        response = table.get_item(
            Key={
                'venueid': event["venueid"],
                'typeid': event["typeid"],
            }
        )

        # get pos id from item
        pos_id = response['Item']['posid']
        creds = response['Item']['poscreds']

        # get menu according to pos_id using venue-specific credentials
        if pos_id == "Odoo":
            return_menu = get_odoo_menu(creds)
        elif pos_id == "Uniware":
            return_menu = get_uniware_menu(creds)
        elif pos_id == "Orbis":
            return_menu = get_orbis_menu(creds)

    except ClientError as e:
        return {
            'statusCode': 404
        }

    if return_menu:
        data = json.dumps(return_menu, indent=4, cls=DecimalEncoder)
        print("Data return is", data)
        return {
            'statusCode': 200,
            'body': data
        }

    else:
        return {
            'statusCode': 404
        }


def get_odoo_menu(creds):
    """Gets the menu of a venue given that it uses the Odoo POS"""
    username = creds[0]  # index defined in database
    password = creds[1]
    url = creds[2]
    db = creds[3]

    # establishing connection to specific venue's POS
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

    # getting only the 'consumable' products from POS
    ids = models.execute_kw(db, uid, password, 'product.product', 'search',
                            [[['available_in_pos', '=', True], ['type', '=', 'consu']]])
    menu = models.execute_kw(db, uid, password, 'product.product', 'read', [ids],
                             {'fields': ['display_name', 'list_price', 'categ_id', 'taxes_id']})

    # in odoo first two IDs are discount and tips so create a new list without them
    food_items = [item for item in menu if
                  item['display_name'] != '[DISC] Discount' and item['display_name'] != '[TIPS] Tips']

    return_menu = {}

    # in Odoo it is compulsory for each food item to be associated with a category
    categs = [x['categ_id'][1] for x in food_items]
    categs = set(categs)

    # return a structured dictionary with the food item and price
    for categ in categs:
        return_menu[categ] = [(item['display_name'], item['list_price']) for item in food_items if
                              item['categ_id'][1] == categ]

    return return_menu


# DUMMY FUNCTIONS UNTIL WE ACTUALLY WORK WITH POS SYSTEMS
def get_uniware_menu(creds):
    return_menu = {}
    return return_menu


def get_orbis_menu(creds):
    return_menu = {}
    return return_menu