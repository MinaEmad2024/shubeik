from .cart import Cart 


# Create context processor for our cart so the car works on all pages of our site
def cart(request):
    #return the default data from our cart 
    return {'cart': Cart(request)}