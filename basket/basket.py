class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in self.session:
            basket = self.session['basket'] = {}
        self.basket = basket

    def add(self, product):
        product_id = product.id
        if product_id not in self.basket:
            self.basket[str(product_id)] = {'price': float(product.price)}
        self.session.modified = True
