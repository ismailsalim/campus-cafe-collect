import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    """Object to format JSON decimals appropriately"""

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
