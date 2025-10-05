from django.core.mail import send_mail
from shubeik import settings
from .models import Order, OrderItem

def send_email( full_name, email, shipping_address, customer_phone,  amount_paid, vendor_email, vendor_watts,  items ):

        # order = Order.objects.get(id = order_id)
        #get order items
        # items = []
        # order_items = OrderItem.objects.filter(order = order)
        # for item in order_items:
        #         items.append(f'اسم المتج: {item.product.name}\n السعر:{item.price}\n الكمية:{item.quantity}\n')

        name = full_name
        customer_email =email
        customer_phone = customer_phone
        address = shipping_address
        total = amount_paid
        vendor_email = vendor_email
        vendor_watts = vendor_watts
        items = items
        all_items = ''.join(items)

        # test_email = 'drmina2007@yahoo.com'
        subject = "Greetings from Shubeik"
        intro = f"Congratulations! You've successfully made a new order from shubeik.\n اسم المشتري:{name} \n العنوان: {address}\n الاجمالي: {total}\n\n\n"
        customer_wattsapp_link = f"واتساب العميل:  https://wa.me/+2{customer_phone}\n\n"
        vendor_wattsapp_link = f"واتساب البائع :   https://wa.me/+2{vendor_watts}\n\n"
        middle = "**** المنتجات المطلوبة **** \n\n"
        message = intro + customer_wattsapp_link + vendor_wattsapp_link +middle + all_items

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [customer_email, vendor_email],
        #     [test_email],
            fail_silently=False,
        )
        
