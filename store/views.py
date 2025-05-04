from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm



def home(request):
    products = Product.objects.all()
    Categories = Category.objects.all() 
    return render(request, 'home.html', {'products':products, 'Categories':Categories})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
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
    return render(request, 'product.html', {'product':product})

def update_user(request):
     if request.user.is_authenticated:
          current_user = User.objects.get(id=request.user.id)
          user_form = UpdateUserForm(request.POST or None, instance=current_user)
          if user_form.is_valid():
               user_form.save()
               login(request, current_user)
               messages.success(request, "User has Been Updated")
               return redirect('home')
          return render(request, "update_user.html", {'user_form': user_form})
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
    #  return render(request, 'update_user.html', {})

def update_info(request):
     if request.user.is_authenticated:
          current_user = Profile.objects.get(user__id=request.user.id)
          form = UserInfoForm(request.POST or None, instance=current_user)
          if form.is_valid():
               form.save()
               messages.success(request, "Your Info has Been Updated")
               return redirect('home')
          return render(request, "update_info.html", {'form': form})
     else:
          messages.success(request, "You Must be Logged in to access this page")
          return redirect('home')
     
def search(request):
     if request.method == "POST":
          searched = request.POST['searched']
          searched = Product.objects.filter(name__icontains=searched)
          #test for null
          if not searched:
               messages.success(request, "That Product doesn't exists, please try agian")
               return render(request,"search.html",{})
          else:
               return render(request,"search.html",{'searched': searched})
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
        return render(request, 'category_summary.html', {'categories':categories})


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