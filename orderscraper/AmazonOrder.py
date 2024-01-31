class AmazonOrder:
    def __init__(self, order_id: str, order_date: str, order_total: float, order_items: list[str]):
        self._order_id = order_id
        self._order_date = order_date
        self._order_total = order_total
        self._order_items = order_items

    ### Properties/Getters ###
    @property
    def order_id(self):
        return self._order_id

    @property
    def order_date(self):
        return self._order_date

    @property
    def order_total(self):
        return self._order_total

    @property
    def order_items(self):
        return self._order_items

    ### Setters ###
    @order_id.setter
    def order_id(self, order_id):
        self._order_id = order_id

    @order_date.setter
    def order_date(self, order_date):
        self._order_date = order_date

    @order_total.setter
    def order_total(self, order_total):
        self._order_total = order_total

    @order_items.setter
    def order_items(self, order_items):
        self._order_items = order_items



