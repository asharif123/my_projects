from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def main_page(request):
    return render(request,'index.html')

def add_account(request):
    errors = Users.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['Password']

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User = Users.objects.create(name=request.POST["Name"],email=request.POST["Email"],street=request.POST["Street"],city=request.POST["City"],state=request.POST["State"],password=pw_hash)
    # Create user's id from the created database, use this to retain info when navigating to another page
    request.session['id'] = User.id
    return redirect('/welcome')

def login(request):
    errors = Users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    User = Users.objects.filter(email=request.POST["Email"])[0]
    if bcrypt.checkpw(request.POST['Password'].encode(), User.password.encode()):
        request.session['id'] = User.id
        return redirect('/welcome')

def welcome_page(request):
    if 'id' not in request.session:
        return redirect('/')
    user = Users.objects.get(id=request.session['id'])
    context = {
        'products': Products.objects.all(),
        'total_products': len(user.products_of_user.all())

    }

    return render(request,'welcome.html',context)

def add_product(request):
    if 'id' not in request.session:
        return redirect('/')

    product = Products.objects.create(name=request.POST["name"],price=request.POST["price"],quantity=request.POST["Quantity"],customer=Users.objects.get(id=request.session['id']))
    return redirect('/welcome')

def logout(request):
    request.session.flush()
    return redirect('/')

def checkout(request):
    if 'id' not in request.session:
        return redirect('/')

    user = Users.objects.get(id=request.session['id'])
    products = user.products_of_user.all()
    total = 0
    if len(products) == 0:
        total = 0
    else:
        for product in products:
            total += (product.price * product.quantity)
        total = total + 10
    context = {
        "products": products,
        "total": total,
        "items": len(products)
    }

    return render(request,'checkout.html',context)

def delete_product(request,id):
    if 'id' not in request.session:
        return redirect('/')
    product_to_delete = Products.objects.get(id=id)
    product_to_delete.delete()
    return redirect('/noorani/checkout')
