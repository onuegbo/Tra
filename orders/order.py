from decimal import Decimal
from etrans.models import TravelProgram


class OrderCreator(object):

     def update_stock_records(self, line):
        """
        Update any relevant stock records for this order line
        """
        if line.product.get_product_class().track_stock:
            line.stockrecord.allocate(line.quantity)
