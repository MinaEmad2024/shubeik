from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import shippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile, Vendor, Category
from .email import send_email
import datetime

# Create your views here.
def admin_dash(request):
        if request.user.is_authenticated and request.user.is_superuser :
            shops = Vendor.objects.all()
            Categories = Category.objects.all() 
            return render(request, 'payment/admin_dash.html', {'shops':shops, 'Categories':Categories})
        else:
            messages.success(request, 'Access Denied')
            return redirect('home')


def admin_orders_dash(request, id):
        if request.user.is_authenticated and request.user.is_superuser:
            orders = Order.objects.filter(vendor__id = id)
            shop = Vendor.objects.get(id=id)
            total = 0
            for order in orders :
                total = total + order.amount_paid

            if request.method == 'POST' :
                start_date = request.POST.get('from')
                end_date = request.POST.get('To')
                # filter orders between 2 dates 
                orders = Order.objects.filter(user__id = id).filter(date_ordered__range=(start_date, end_date))
                total = 0
                for order in orders :
                    total = total + order.amount_paid
                return render(request, 'payment/admin_orders_dash.html', {"orders": orders, "total": total, "id": id, "shop": shop, 'start_date':start_date, 'end_date':end_date})

            return render(request, 'payment/admin_orders_dash.html', {"orders": orders, "total": total, "id": id , "shop": shop})
        else:
            messages.success(request, 'Access Denied')
            return redirect('home')
def orders(request, pk):
        
        if request.user.is_authenticated :
            # get order
            order =  Order.objects.get(id=pk)
            
            # Prevent other users from accessing current user data
            if order.user == request.user or request.user.is_superuser:
                # get order items
                items = OrderItem.objects.filter(order=pk)

                if request.POST:
                    status = request.POST['shipping_status']
                    if status == 'true':
                        order = Order.objects.filter(id=pk)
                        now = datetime.datetime.now()
                        order.update(shipped = True, date_shipped=now)
                        
                    else:
                        order = Order.objects.filter(id=pk)
                        order.update(shipped = False)

                    messages.success(request, "Shipping Status Updated")
                    return redirect('home')


                return render(request, 'payment/orders.html', {'order':order, 'items':items})
            else:
                messages.success(request, 'Your Are not Authorized to access this Page')
                return redirect('home')


        else:
            messages.success(request, 'Access Denied')
            return redirect('home')


def shipped_dash(request):
        if request.user.is_authenticated :
            orders = Order.objects.filter(shipped = True).filter(user__id = request.user.id)

            if request.POST:
                status = request.POST['shipping_status']
                num = request.POST['num']
                order = Order.objects.filter(id=num)
                now = datetime.datetime.now()
                order.update(shipped = False)
                    
                messages.success(request, "Shipping Status Updated")
                return redirect('home')
            return render(request, 'payment/shipped_dash.html', {"orders": orders})
        else:
            messages.success(request, 'Access Denied')
            return redirect('home')


def not_shipped_dash(request):
        if request.user.is_authenticated :
            orders = Order.objects.filter(shipped = False).filter(user__id = request.user.id)

            if request.POST:
                status = request.POST['shipping_status']
                num = request.POST['num']
                order = Order.objects.filter(id=num)
                now = datetime.datetime.now()
                order.update(shipped = True , date_shipped=now)
                    
                messages.success(request, "Shipping Status Updated")
                return redirect('home')
            return render(request, 'payment/not_shipped_dash.html', {"orders": orders})
        else:
            messages.success(request, 'Access Denied')
            return redirect('home')

def process_order(request, category):
    if request.POST:
        # get the cart 
        cart = Cart(request)
        cart_products = cart.get_products(category=category)
        quantities = cart.get_quants(category=category)
        totals = cart.cart_total(category=category)
        #Get the vendor id 
        vendor = Vendor.objects.get(name = category)     
        vendor_email = vendor.email   
        vendor_watts = vendor.watts_app
        # gett billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session data
        my_shipping = request.session.get('my_shipping')
        # print(my_shipping)
        # gather order info 
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        customer_phone = my_shipping['shipping_zipcode']
        # Create shipping address from session info 
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        # print(shipping_address)
        amount_paid = totals
        #logged in user 
        if request.user.is_authenticated:
            #loged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, vendor=vendor)
            # create_order.save()
            
            # add order items
            #get the order ID
            order_id = create_order.pk
            # get product info
            for product in cart_products:
                # get product id
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # get quantity
                items = []
                for key , value in quantities.items():
                    if int(key) == product.id:
                        #create order item
                        items.append(f'اسم المتج: {product.name}\n السعر:{price}\n الكمية:{value}\n')
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id ,user=user, quantity=value , price=price)
                        # create_order_item.save()
                        # send order to the user and vendor
            #send a confirmation email
            items = items
            send_email(full_name, email, shipping_address, customer_phone,  amount_paid, vendor_email, vendor_watts,  items )

            # delete the cart
            # for key in list(request.session.keys()):
            #     if key == "session_key":
            #         # delete the key
            #         del request.session[key]
            new_cart = []
            for key in request.session["session_key"].items():
                # print(key)
                for product in cart_products:
                    # print(product.id)
                    if product.id == int(key[0]):
                        # del request.session["session_key"][key[0]]
                        new_cart.append(key)
                        # print(new_cart_2)
            new_cart_2 = dict(new_cart)
            new_cart_3 = request.session["session_key"]
            for key in new_cart_2:
                new_cart_3.pop(key, None)
            # request.session["session_key"] = new_cart_2
            request.session["session_key"] = new_cart_3
            print(request.session["session_key"])

            # delete cart from database(old cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database
            carty = str(new_cart_3)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart= str(carty))
            messages.success(request, 'Order Placed!')
            return redirect('home')
        
        else:
            # not logged in
            create_order = Order( full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, vendor=vendor)
            # create_order.save()

            # add order items
            #get the order ID
            order_id = create_order.pk
            # get product info
            for product in cart_products:
                # get product id
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                # get quantity
                items = []
                for key , value in quantities.items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value , price=price)
                        items.append(f'اسم المتج: {product.name}\n السعر:{price}\n الكمية:{value}\n')
                        # create_order_item.save()
            #send a confirmation email
            items = items
            send_email(full_name, email, shipping_address, customer_phone,  amount_paid, vendor_email, vendor_watts,  items )


            # delete the cart
            # for key in list(request.session.keys()):
            #     if key == "session_key":
            #         # delete the key
            #         del request.session[key]
            new_cart = []
            for key in request.session["session_key"].items():
                # print(key[0])
                for product in cart_products:
                    # print(product.id)
                    if product.id == int(key[0]):
                        # del request.session["session_key"][key[0]]
                        new_cart.append(key)
                        # print(new_cart_2)
            new_cart_2 = dict(new_cart)
            new_cart_3 = request.session["session_key"]
            for key in new_cart_2:
                new_cart_3.pop(key, None)
            # request.session["session_key"] = new_cart_2
            request.session["session_key"] = new_cart_3
            messages.success(request, 'Order Placed!')
            return redirect('home')
        
        # messages.success(request, 'Order Placed!')
        # return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')

def billing_info(request, category):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products(category=category)
        quantities = cart.get_quants(category=category)
        totals = cart.cart_total(category=category)
        # create a session with shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping 
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form, 'category': category})
        else:
            billing_form = PaymentForm()
            print(request.session)
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form, 'category': category})


        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'shipping_form':shipping_form})
    else :
        messages.success(request, 'Access denied')
        return redirect('home')


def checkout(request, category):
    cart = Cart(request)
    cart_products = cart.get_products(category=category)
    quantities = cart.get_quants(category=category)
    totals = cart.cart_total(category=category)
    if request.user.is_authenticated:
        # checkout as logged in user
        shipping_user = shippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'shipping_form':shipping_form, 'category': category})
        #checkout as guest
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities':quantities,'totals':totals, 'shipping_form':shipping_form, 'category': category})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
