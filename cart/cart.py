from store.models import Product 
from django.contrib.sessions.models import Session


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request 
        #self.request = request

        # Get he current user sessionkey if exists
        cart = self.session.get('session_key')
        # k = k = Session.objects.get(pk=self.session.get('session_key'))
        # print(k.get_decoded())


        #if the user is new, no session key create one!
        if 'session.key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure the cart is available on all pages of the site
        self.cart = cart 

    def add(self, product):
        product_id = str(product.id)

        #logic
        if product_id in self.cart:
            pass

        else:
            self.cart[product_id] = { 'price': str(product.price)}

        self.session.modified = True


    def __len__(self):
        return len(self.cart)


    def get_products(self):
        #Get ids from cart
        products_ids = self.cart.keys()

        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=products_ids)

        #return looked_up products 
        return products 
