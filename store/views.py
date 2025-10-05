from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Vendor, Review
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, CategoryForm, VendorForm, Product_Form
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import shippingAddress


def home(request):
     if request.method == "POST":
          searched = request.POST['searched']
          searched_p = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
          searched_c = Category.objects.filter(Q(name__icontains=searched))
          searched_v = Vendor.objects.filter(Q(name__icontains=searched) | Q(category__icontains=searched))
          print(searched_v)
          #test for null
          if not searched_p and not searched_c and not searched_v:
               messages.success(request, "That Product doesn't exists, please try agian")
               return render(request,"search.html",{})
          else:
               return render(request,"search.html",{"searched_key":searched ,'searched': searched_p, "categories": searched_c, "shops": searched_v})

     else:
          shops = Vendor.objects.all()
          Categories = Category.objects.all() 
          return render(request, 'shops.html', {'shops':shops, 'Categories':Categories})

def view_shop_generic(request, id):
          shop = Vendor.objects.get(id=id)
          products = Product.objects.filter(vendor=id)
          return render(request, "view_shop_generic.html", {"products":products, "shop":shop})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
            # do shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from database
            saved_cart = current_user.old_cart
            #convert db string to python dictionary 
            if saved_cart:
               #convert to dictionary using json 
               converted_cart = json.loads(saved_cart)
               #add the loaded cart dictionary to our session 
               cart = Cart(request)
               # loop through the cart and add the items from the dictionary 
               for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)




            messages.success(request, "Logged in successfully ")
            return redirect('home')
        else :
            messages.success(request, "Error try again  ")
            return redirect('login')

    else:
        return render(request, 'login.html', {})    
     
def logout_user(request):
    logout(request)
    messages.success(request, ("logout successfully"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (" User is created, please fill in the Info below..... "))
            return redirect("update_info")
        else:
            messages.success(request, (" try again "))
            return redirect("register")    
    else:
        return render(request, 'register.html', {'form':form})


def product(request, pk):
     product = Product.objects.get(id=pk)
     reviews = Review.objects.filter(post=product)
     # calculate user rating for each product
     if reviews:
          Rating_a = 0
          i = 0
          # get totatl of all ratings for that product
          for review in reviews :
               Rating_a = Rating_a + review.rating
               i = i + 1 
          # get a medium of the rating
          rating_A = Rating_a / i
          #check for the first decimal place
          decimal = str(rating_A) 
          if '.' in decimal and int(decimal.split('.')[1]) > 0:
               half_star = True
               rating_A = int((rating_A))
               rating_B = range(4 - (rating_A))
               rating_A = range(rating_A)
          else:
               half_star = False
               rating_A = int((rating_A))
               rating_B = range(5 - (rating_A))
               rating_A = range(rating_A)
     # No Rating yet
     else:
          rating_A = range(0)
          rating_B = range(5)
          half_star = False
     # make a pis
     if request.method == "POST" and request.user.is_authenticated:
          #check if a rating or review exists in the POST
          try:     
               rating =request.POST['rating']
               review = request.POST['review']
          except:
               rating = ''
               review = ''                
          # create a comment if a rating and reviews exists
          if rating and review :
               user = User.objects.get(id = request.user.id)
               name = user.first_name
               email = user.email
               Review.objects.create(
                    post=product,
                    name=name,
                    email=email,
                    body=review,
                    rating=rating
               )  
               return render(request, 'product.html', {'product':product, 'reviews':reviews, 'rating_A':rating_A, "rating_B":rating_B, 'half_star':half_star })
          else:
               messages.success(request, "برجاء  كتابة تعليق و اختيار عدد من النجوم للتقييم ")
               return render(request, 'product.html', {'product':product, 'reviews':reviews, 'rating_A':rating_A, "rating_B":rating_B, 'half_star':half_star })

     else:
          product = Product.objects.get(id=pk)
          reviews = Review.objects.filter(post=product)      
          return render(request, 'product.html', {'product':product, 'reviews':reviews, 'rating_A':rating_A, "rating_B":rating_B,  'half_star':half_star })

def update_user(request):
     if request.user.is_authenticated:
          current_user = User.objects.get(id=request.user.id)
          user_form = UpdateUserForm(request.POST or None, instance=current_user)
          user = Profile.objects.get(user=request.user.id)
          # if request.user.is_superuser:
          #      shops = Vendor.objects.filter(owner = request.user.id)
          # else:
          shops = Vendor.objects.filter(owner = user)

          print(shops)
          if user_form.is_valid():
               user_form.save()
               login(request, current_user)
               messages.success(request, "User has Been Updated")
               return redirect('home')
          return render(request, "update_user.html", {'user_form': user_form, 'shops':shops})
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
    #  return render(request, 'update_user.html', {})

def update_info(request):
     if request.user.is_authenticated:
          # get current user
          current_user = Profile.objects.get(user__id=request.user.id)
          # get current user's shipping info
          shipping_user = shippingAddress.objects.get(user__id=request.user.id)

          # get original User Form
          form = UserInfoForm(request.POST or None, instance=current_user)
          # get user's shippingForm
          shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

          if form.is_valid() or shipping_form.is_valid():
               #save original form 
               form.save()
               # save shipping form 
               shipping_form.save()
               messages.success(request, "Your Info has Been Updated")
               return redirect('home')
          return render(request, "update_info.html", {'form': form, 'shipping_form':shipping_form})
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
     
def search(request):
     if request.method == "POST":
          searched = request.POST['searched']
          searched_p = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
          searched_c = Category.objects.filter(Q(name__icontains=searched))
          searched_v = Vendor.objects.filter(Q(name__icontains=searched) | Q(category__icontains=searched))

          #test for null
          if not searched_p and not searched_c and not searched_v:
               messages.success(request, "That Product doesn't exists, please try agian")
               return render(request,"search.html",{})
          else:
               return render(request,"search.html",{"searched_key":searched ,'searched': searched_p, "categories": searched_c, "shops": searched_v})
     else:
          return render(request,"search.html",{})
     
     
def update_password(request):
     if request.user.is_authenticated:
          current_user = request.user
          if request.method == "POST":
               form = ChangePasswordForm(current_user, request.POST)
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Your Password Has Been Updated, please Log In')
                    return redirect('login')
               else:
                    for error in list(form.errors.values()):
                         messages.error(request, error)
                         return redirect('update_password')

          else:
               form = ChangePasswordForm(current_user)
               return render(request, 'update_password.html', {'form':form})
     else:
        messages.success(request, "You Must be Logged IN To veiw This Page")
        return redirect('home')


def category_summary(request):
        categories = Category.objects.all()
        category_form = CategoryForm(request.POST or None)
        if request.method == 'POST':
               if category_form.is_valid():
                    category_form.save()
                    messages.success(request, 'You Added a new category successfuly')
                    return redirect('category_summary')
               else:
                    for error in list(category_form.errors.values()):
                         messages.error(request, error)
                         return redirect('category_summary')

        else:
             return render(request, 'category_summary.html', {'categories':categories, 'category_form':category_form})


def category(request, foo):
        # foo = foo.replace("-", " ")
        # foo = foo.capitalize()
        # print(foo)
        category = Category.objects.get(name=foo)
        # print(category.name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
        # try:
        #     category = Category.objects.get(name=foo)
        #     # category = foo
        #     products = Product.objects.filter(category=category)
        #     return render(request, 'category.html', {'products':products, 'category':category})

        # except:
        #     messages.success(request, (" that category doesn't exist "))
        #     return redirect('home')

def add_new_product(request, id):
     if request.user.is_authenticated:
          user = Profile.objects.get(user=request.user.id)
          shops = Vendor.objects.filter(id = request.user.id)
          product_form = Product_Form(request.POST or None , request.FILES,  request=request)# , initial={'vendor': vendor.id}) 
          if request.method == 'POST':
               # get product vendor
               owner = Profile.objects.get(user=request.user)
               if product_form.is_valid():
                    new_product = product_form.save(commit=False)
                    new_product.vendor = Vendor.objects.get(id = id)
                    new_product.save()
                    messages.success(request, 'You Added a new Product successfuly')
                    return redirect('update_user')
               else:
                    for error in list(product_form.errors.values()):
                         print(request.body)
                         messages.error(request, error)
                         return redirect('update_user')
          else:     
               return render(request, "add_new_product.html", {"product_form": product_form} )
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')

def edit_product(request, id):
     if request.user.is_authenticated:
          product = Product.objects.get(id=id)
          shop_id = product.vendor.id
          # Prevent other users from accessing current user data
          if request.user == product.vendor.owner.user:

               # print(shop_id)
               product_form = Product_Form(request.POST or None,  instance=product,  request=request) 
               if request.method == 'POST':
                    # get product vendor 
                    owner = Profile.objects.get(user=request.user)
                    # product_image = request.FILES['image']
                    ## check existence of a new product photo
                    if 'image' in request.FILES:
                         product_image = request.FILES['image']
                         if product_form.is_valid():
                              edited_product = product_form.save(commit=False)
                              edited_product.image = product_image
                              edit_product.vendor = Vendor.objects.get(id = shop_id)
                              edited_product.save()
                              messages.success(request, "Shop has Been Updated")
                              return redirect('update_user')
                    
                         else:
                              for error in list(product_form.errors.values()):
                                   print(request.body)
                                   messages.error(request, error)
                                   return redirect('update_user')
                    else:
                         if product_form.is_valid():
                              edited_product = product_form.save(commit=False)
                              # edited_product.image = product_image
                              edit_product.vendor = Vendor.objects.get(id = shop_id)
                              edited_product.save()
                              messages.success(request, "Shop has Been Updated")
                              return redirect('update_user')
                    
                         else:
                              for error in list(product_form.errors.values()):
                                   print(request.body)
                                   messages.error(request, error)
                                   return redirect('update_user')

               else:
                    return render(request, "edit_product.html", {"product_form": product_form, 'shop_id': shop_id, 'product':product})
          else:
               messages.success(request, "You are UNAUTHORIZED to access this page")
               return redirect('home')

     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
     
def view_shop(request, id):
     shop_id = id
     if request.user.is_authenticated:
          vendor = Vendor.objects.get(id=id)
          products = Product.objects.filter(vendor=id)
          # Prevent other users from accessing current user data
          if request.user == vendor.owner.user:
               return render(request, "view_shop.html", {"products":products, "shop_id":shop_id})
          else:
               messages.success(request, "You are UNAUTHORIZED to access this page")
               return redirect('home')
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')


def add_new_shop(request):
     if request.user.is_authenticated:
          current_user = Profile.objects.get(user__id=request.user.id)
          print(current_user)
          vendorform = VendorForm(request.POST or None, request.FILES, request=request ) #, initial={'owner': current_user.id})#(request.POST or None)
          # vendorform.fields['owner'] = current_user
          if request.method == 'POST':
               if vendorform.is_valid():
                    new_shop = vendorform.save(commit=False)
                    new_shop.owner =  Profile.objects.get(user= request.user)
                    new_shop.save()
                    # instance = vendorform.save(commit=False)
                    # instance.user = request.user
                    # instance.save()
                    messages.success(request, 'You Added a new shop successfuly')
                    return redirect('update_user')
               else:
                    for error in list(vendorform.errors.values()):
                         print(request.body)
                         messages.error(request, error)
                         return redirect('add_new_shop')
          else:     
               return render(request, "add_new_shop.html", {"vendorform":vendorform})
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')

#edit current shop
def my_shop(request, id):

     if request.user.is_authenticated:
               shop = Vendor.objects.get(id=id)
               # print(shop.__dict__ )    
               # vendorform.fields['owner'].queryset = Vendor.objects.filter(owner=request.user.id)

               # Prevent current user from accessing other users data
               if request.user == shop.owner.user:

                    vendorform = VendorForm(request.POST or None, instance=shop, request=request)
                    # check if a new photo is added 
                    if request.method == 'POST' and 'image' in request.FILES :
                              shop_image = request.FILES['image']
                              if vendorform.is_valid():
                                   edited_shop = vendorform.save(commit=False)
                                   edited_shop.image = shop_image
                                   edited_shop.owner = Profile.objects.get(user=request.user)
                                   edited_shop.save()
                                   messages.success(request, "Shop has Been Updated")
                                   return redirect('update_user')
                    # no new photo is added 
                    elif request.method == 'POST':
                              if vendorform.is_valid():
                                   edited_shop = vendorform.save(commit=False)
                                   edited_shop.owner = Profile.objects.get(user=request.user)
                                   edited_shop.save()
                                   messages.success(request, "Shop has Been Updated")
                                   return redirect('update_user')
                    else:
                         return render(request, "my_shop.html", {"vendorform":vendorform, "shop": shop})
               else:
                    messages.success(request, "You are UNAUTHORIZED to access this page")
                    return redirect('home')

     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
