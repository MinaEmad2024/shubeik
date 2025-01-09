from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
# Create your views here.


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
            messages.success(request, (" Success "))
            return redirect("home")
        else:
            messages.success(request, (" try again "))
            return redirect("register")    
    else:
        return render(request, 'register.html', {'form':form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

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