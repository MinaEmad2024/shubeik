from django.shortcuts import render, get_object_or_404
from .cart import Cart 
from store.models import Product
from django.http  import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request, category):
    cart = Cart(request)
    cart_products = cart.get_products(category=category)
    quantities = cart.get_quants(category=category)
    totals = cart.cart_total(category=category)
    return render(request, 'cart_summary.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'category' :category})
    

def cart_vendors(request) :

    cart= Cart(request)
    cart_products = cart.get_all_products()
    categories = [] # get all categories from the cart items
    for product in cart_products:
        categories.append(product.vendor)
    new_categories = set(categories)
    return render(request, 'vendors.html', {"categories":new_categories})


def cart_add(request):
    # get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':

        #get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity = product_qty) 

        #  get cart quantity 
        cart_quantity = cart.__len__()


        #Return a response
        #response = JsonResponse({'Product Name :': product.name })
        response = JsonResponse({'qty' : cart_quantity})
        messages.success(request,("Product Added to Cart ..."))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        # call delete function in the cart
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request,("Product deleted from the shopping Cart ..."))

        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))
        # print(request.POST.get('product_qty'))
        product_qty = int(request.POST.get('product_qty'))
                                                    
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request,("Shopping Cart has been updated ..."))
        return response
        # return redirect('cart_summary')