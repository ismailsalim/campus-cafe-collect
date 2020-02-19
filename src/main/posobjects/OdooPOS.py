import xmlrpc.client
from main.posobjects.BasePOS import BasePOS


class OdooPOS(BasePOS):
    def __init__(self, venueID, creds):
        super().__init__(venueID)
        self.POStype = 'Odoo'
        self.username = creds[0]  # index defined in database
        self.password = creds[1]
        self.url = creds[2]
        self.db = creds[3]
        self.conn = None
        self.uid = None

    def getConnection(self):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            self.conn = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            self.conn.execute_kw(self.db, self.uid, self.password,
                                   'res.partner', 'check_access_rights',
                                   ['read'], {'raise_exception': False})
        except Exception as e: # think what to do here
            raise OdooAPIException(e)

    def getMenu(self):
        self.getConnection()
        ids = self.conn.execute_kw(self.db, self.uid, self.password, 'product.product', 'search',
                                     [[['available_in_pos', '=', True], ['type', '=', 'consu']]])
        return self.formatMenu(
            self.conn.execute_kw(self.db, self.uid, self.password, 'product.product', 'read', [ids],
                                   {'fields': ['display_name', 'list_price', 'categ_id']}))

    def formatMenu(self, menu):
        if len(menu) == 0:
            raise RuntimeError(f"No menu returned from POS {self, self.db, self.url}")

        # in Odoo first two IDs are discount and tips so create a new list without them
        food_items = [item for item in menu if
                      item['display_name'] != '[DISC] Discount' and item['display_name'] != '[TIPS] Tips']

        return_menu = {}

        # in Odoo it is compulsory for each food item to be associated with a category
        categs = [x['categ_id'][1] for x in food_items]
        categs = set(categs)

        # return a structured dictionary with the food item name and price
        for categ in categs:
            return_menu[categ] = [(item['display_name'], item['list_price']) for item in food_items if
                                  item['categ_id'][1] == categ]

        return return_menu

    def __str__(self):
        return self.POStype


class OdooAPIException(Exception):
    pass
