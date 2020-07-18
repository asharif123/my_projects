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
    # product = Products.objects.create(name="Ground Beef Curry", price=1.49, image="ground_beef.JPG")
    # product = Products.objects.create(name="Chicken Curry", price=1.49, image="chicken.JPG")
    
    context = {
        "products": Products.objects.all(),
        "total_orders": len(user.orders_of_user.all())
    }


    return render(request,'welcome.html',context)

def add_order(request):
    if 'id' not in request.session:
        return redirect('/')
    product = Products.objects.get(id=request.POST["product"])
    user = Users.objects.get(id=request.session['id'])
    order = Orders.objects.create(quantity=request.POST['Quantity'],customer=user)
    order.product.add(product)
    return redirect('/noorani/checkout')

def logout(request):
    request.session.flush()
    return redirect('/')

def checkout(request):
    if 'id' not in request.session:
        return redirect('/')
    user = Users.objects.get(id=request.session['id'])
    products = []
    for order in user.orders_of_user.all():
        for product in order.product.all():
            products.append(product)
    quantities = []
    for order in user.orders_of_user.all():
        quantities.append(order.quantity)
    total = 0

    for i in range(len(products)):
        total += products[i].price*quantities[i]
    context = {
        "user": user,
        "total_orders": len(user.orders_of_user.all()),
        "Orders": user.orders_of_user.all(),
        "total": total + 10        }
    return render(request,'checkout.html',context)

def delete_product(request,id):
    if 'id' not in request.session:
        return redirect('/')
    product_to_delete = Products.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    for order in user.orders_of_user.all():
        for product in order.product.all():
            if product == product_to_delete:
                order.delete()
                return redirect('/noorani/checkout')

    

def delete_all(request):
    if 'id' not in request.session:
        return redirect('/')

    user = Users.objects.get(id=request.session['id'])
    user.orders_of_user.all().delete()
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
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }
    return render(request,'account_details_ajax.html',context)


    
