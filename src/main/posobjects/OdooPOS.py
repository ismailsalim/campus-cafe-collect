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
        self.session_id = None
        self.order_id = None

    def getConnection(self):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            self.conn = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            self.conn.execute_kw(self.db, self.uid, self.password,
                                 'res.partner', 'check_access_rights',
                                 ['read'], {'raise_exception': False})
            self.session_id = self.conn.execute_kw(self.db, self.uid, self.password,
                                                   'pos.session', 'search', [[['state', '=', 'opened']]]
                                                   )
        except Exception as e:  # think what to do here
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

    def createOrder(self):
        self.order_id = self.conn.execute_kw(self.db, self.uid, self.password,
                                             'pos.order', 'create', [{'session_id': self.session_id[0],
                                                                      'amount_tax': 0, 'amount_total': 0,
                                                                      'amount_paid': 0, 'amount_return': 0}])

    def pushOrder(self, order):
        self.getConnection()
        self.createOrder()

        processedOrder = []
        for product in order:
            price = float(order[product]['price'])
            quantity = float(order[product]['quantity'])
            name = order[product]['username']
            priceSubtotal = price * quantity
            priceSubtotaIncl = priceSubtotal * self.vat
            processedOrder.append(
                {'qty': quantity, 'price_subtotal': priceSubtotal, 'price_subtotal_incl': priceSubtotaIncl,
                 'order_id': self.order_id, 'price_unit': price, 'product_id': product})
        subtotal = 0
        subtotalIncl = 0

        for product in processedOrder:
            subtotal += product['price_subtotal']
            subtotalIncl += product['price_subtotal_incl']
        amountTax = subtotalIncl - subtotal

        self.conn.execute_kw(self.db, self.uid, self.password, 'pos.order.line', 'create', [processedOrder])
        reference = str(self.session_id) + "-" + str(self.order_id) + " " + name
        self.conn.execute_kw(self.db, self.uid, self.password, 'pos.order', 'write',
                             [self.order_id, {'pos_reference': reference,
                                              'amount_tax': amountTax,
                                              'amount_total': subtotalIncl,
                                              'amount_paid': subtotalIncl,
                                              'amount_return': 0,
                                              'state': 'paid'}])
        return reference

    def __str__(self):
        return self.POStype


class OdooAPIException(Exception):
    pass
