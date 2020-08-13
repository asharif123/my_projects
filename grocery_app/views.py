from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *
import urllib.request
import json


# Create your views here.
def main_page(request):
    return render(request,'index.html')

def add_account(request):
    errors = Users.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
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
        return redirect('/home')
    User = Users.objects.filter(email=request.POST["Email"])[0]
    if bcrypt.checkpw(request.POST['Password'].encode(), User.password.encode()):
        request.session['id'] = User.id
        return redirect('/welcome')

def welcome_page(request):

    if 'id' not in request.session:
        total_orders = 0
    else:
        user = Users.objects.get(id=request.session['id'])
        total_orders = len(user.orders_of_user.all())

    
    context = {
        "products": Products.objects.all(),
        "total_orders": total_orders,
        "user": user,
        'liked_products': user.liked_products.all()
    }

    return render(request,'welcome.html',context)

def liked_product(request,id):
    if 'id' not in request.session:
        return redirect('/home')
    user = Users.objects.get(id=request.session['id'])
    product = Products.objects.get(id=id)
    liked_product = product.users_who_like.add(user)
    return redirect('/welcome')

def unliked_product(request,id):
    if 'id' not in request.session:
        return redirect('/home')
    user = Users.objects.get(id=request.session['id'])
    product = Products.objects.get(id=id)
    liked_product = product.users_who_like.remove(user)
    return redirect('/welcome')

def favorites(request):
    return render(request,'favorite_items.html')

def add_order(request):
    if 'id' not in request.session:
        return redirect('/home')
    product = Products.objects.get(id=request.POST["product"])
    user = Users.objects.get(id=request.session['id'])
    order = Orders.objects.create(quantity=request.POST['Quantity'],customer=user)
    order.product.add(product)
    return redirect('/noorani/checkout')

def logout(request):
    request.session.flush()
    return redirect('/home')

def checkout(request):
    if 'id' not in request.session:
        return redirect('/home')
    user = Users.objects.get(id=request.session['id'])
    origin = '14178 Brookhurst St, Garden Grove, CA 92843'
    origin = origin.replace(' ','+')
    destination = '{},{},{},{}'.format(user.street, user.city, user.state, user.zipcode)
    destination = destination.replace(' ','+')

# Grab Google directions api info from Google maps uRL
    api_key = 'AIzaSyBm9ZKXq83YFy9BLQQe50vXS-QHYedkvvw'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    new_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
    my_request = endpoint+new_request
    response = urllib.request.urlopen(my_request).read()
    directions = json.loads(response)
    lattitude = (directions['routes'][0]['legs'][0]['end_location']['lat'])
    longitude = (directions['routes'][0]['legs'][0]['end_location']['lng'])

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
        "total": total + 10,
        "lattitude": lattitude,
        "longitude": longitude
    }
        
    return render(request,'checkout.html',context)

def delete_product(request):
    if 'id' not in request.session:
        return redirect('/home')
    user = Users.objects.get(id=request.session['id'])


    product_to_delete = Products.objects.get(id=request.POST["product_id"])
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

    for order in user.orders_of_user.all():
        for product in order.product.all():
            if product == product_to_delete:
                order.delete()
                return redirect('/noorani/checkout')

    

def delete_all(request):
    if 'id' not in request.session:
        return redirect('/home')

    user = Users.objects.get(id=request.session['id'])
    user.orders_of_user.all().delete()
    return redirect('/welcome')

def account_page(request):
    if 'id' not in request.session:
        return redirect('/home')
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }
    return render(request,'account.html',context)

def charge(request):
    if 'id' not in request.session:
        return redirect('/home')
    return redirect('/noorani/success')

def success(request):
    if 'id' not in request.session:
        return redirect('/home')
    user = Users.objects.get(id=request.session['id'])
    user.orders_of_user.all().delete()
    context = {
        "user": user
    }

    return render(request,'success.html',context)

def account_info(request):
    if 'id' not in request.session:
        return redirect('/home')
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }

    return render(request,'account_details.html',context)

def update_account(request):
    if 'id' not in request.session:
        return redirect('/home')
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

def checkout_page(request):
    context = {
        "user": Users.objects.get(id=request.session['id'])
    }

    return render(request,'checkout_page.html',context)


    
