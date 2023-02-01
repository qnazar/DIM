from decimal import Decimal

from school.models import Abonement


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in self.session:
            basket = self.session['basket'] = {}
        self.basket = basket

    def add(self, product, quantity):
        product_id = product.id
        if product_id not in self.basket:
            self.basket[str(product_id)] = {'price': float(product.price),
                                            'quantity': int(quantity)}
        else:
            self.basket[product_id]['quantity'] = quantity
        self.save()

    def update(self, product_id: str, quantity: int):
        """
        Update values in session data
        """
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = quantity
        self.save()

    def delete(self, product_id: str):
        """
        Delete item from session data
        """
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        abonement_ids = [int(key) for key in self.basket.keys()]
        abonements = Abonement.objects.filter(id__in=abonement_ids)
        basket = self.basket.copy()

        for abonement in abonements:
            basket[str(abonement.id)]['abonement'] = abonement

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Get the basket data and count the quantity of items
        :return: int
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
