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
    User = Users.objects.create(name=request.POST["Name"],email=request.POST["Email"],street=request.POST["Street"],city=request.POST["City"],state=request.POST["State"],zipcode=request.POST["Zip"],password=pw_hash)
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
        "items": len(products),
        "user": user
    }

    return render(request,'checkout.html',context)

def delete_product(request,id):
    if 'id' not in request.session:
        return redirect('/')
    product_to_delete = Products.objects.get(id=id)
    product_to_delete.delete()
    return redirect('/noorani/checkout')

    

def delete_all(request):
    if 'id' not in request.session:
        return redirect('/')

    user = Users.objects.get(id=request.session['id'])
    delete_products = user.products_of_user.all().delete()
    return redirect('/welcome')

def account_page(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }
    return render(request,'account.html',context)

def submit(request):
    if 'id' not in request.session:
        return redirect('/')
    errors = Card.objects.card_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/noorani/checkout')

    card = Card.objects.create(name=request.POST["name"],card_number=request.POST["cardnumber"],expiration=request.POST["cardexpiration"],card_code=request.POST["cardcvv"],owner=Users.objects.get(id=request.session['id']))
    return redirect('/noorani/success')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }

    return render(request,'success.html',context)

def account_info(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }

    return render(request,'account_details.html',context)

def update_account(request):
    if 'id' not in request.session:
        return redirect('/')
    errors = Users.objects.account_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account/info')
    User_update = Users.objects.get(id=request.session['id'])
    User_update.password = request.POST['Password']

    pw_hash = bcrypt.hashpw(User_update.password.encode(), bcrypt.gensalt()).decode()
    User_update.name = request.POST["Name"]
    User_update.email = request.POST["Email"]
    User_update.street = request.POST["Street"]
    User_update.city = request.POST["City"]
    User_update.state = request.POST["State"]
    User_update.zip = request.POST["Zip"]
    User_update.password = pw_hash
    User_update.save()

    # Create user's id from the created database, use this to retain info when navigating to another page
    request.session['id'] = User_update.id
    return redirect('/welcome')


    
