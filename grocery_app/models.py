from PIL import Image
import bcrypt, re
from django.db import models
from datetime import datetime
now = datetime.now()


class Users_Manager(models.Manager):

    def registration_validator(self, postData):
        errors = {}

        if len(postData["Name"]) < 2:
            errors["Name"] = "Name must have at least 2 characters!"

        # see if email is either in correct format or in the database
        REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX.match(postData['Email']):                
            errors['Email'] = ("Invalid email address format!")

        email = Users.objects.filter(email=postData["Email"])
        if len(email) > 0:
            errors["Email"] = ("Account already exists!")

        if len(postData["Street"]) < 5:
            errors["Street"] = ("Street should have at least 5 characters!")
                
        if len(postData["City"]) < 5:
            errors["City"] = ("City should have at least 5 characters!")

        if len(postData["State"]) < 3:
            errors["State"] = ("State should have at least 3 characters!")

        if len(postData["Zip"]) != 5:
            errors["Zip"] = ("Zipcode must have at least 5 digits!")


        if len(postData["Password"]) < 8:
            errors["Password"] = ("Password must be at least 8 characters!")

        if (postData["Password"] != postData["Confirm"]):
            errors["Password"] = ("Password and Confirm password do not match!")

        return errors
    def account_validator(self, postData):
        errors = {}

        if len(postData["Name"]) < 2:
            errors["Name"] = "Name must have at least 2 characters!"

        # see if email is either in correct format or in the database
        REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX.match(postData['Email']):                
            errors['Email'] = ("Invalid email address format!")

        if len(postData["Street"]) < 5:
            errors["Street"] = ("Street should have at least 5 characters!")
                
        if len(postData["City"]) < 5:
            errors["City"] = ("City should have at least 5 characters!")

        if len(postData["State"]) < 3:
            errors["State"] = ("State should have at least 3 characters!")

        if len(postData["Zip"]) != 5:
            errors["Zip"] = ("Zipcode must have at least 5 digits!")

        if len(postData["Password"]) < 8:
            errors["Password"] = ("Password must be at least 8 characters!")

        if (postData["Password"] != postData["Confirm"]):
            errors["Password"] = ("Password and Confirm password do not match!")

        return errors


    def login_validator(self,postData):
        errors = {}

        REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX.match(postData["Email"]):                
            errors['Email'] = ("Invalid email address format!")

        if len(postData["Password"]) < 8:
            errors["Password"] = ("Password must be at least 8 characters!")

        # check if login email is in the database!
        #if login email in database, see if the password entered matches to stored password for that email in the database
        user = Users.objects.filter(email=postData["Email"])

        if len(user) == 0:
            errors["Email"] = ("Email does not exists, please register or try a different account!")

        else:
            user = Users.objects.filter(email=postData["Email"])[0]
            if not bcrypt.checkpw(postData["Password"].encode(), user.password.encode()):
                errors["Password"] = ("Password is incorrect!")

        return errors

class Cards_Manager(models.Manager):
    def card_validator(self,postData):
        errors = {}
        if len(postData["name"]) < 2:
            errors["name"] = "Name must have at least 2 characters!"

        if not (postData["name"].isalpha()):
            errors["name"]: "Card name must have all letters!"

        if len(postData["cardnumber"]) != 16:
            errors["cardnumber"] = "Credit Card number must have 16 digits!"

        if not (postData["cardnumber"]).isnumeric():
            errors["cardnumber"] = "Card Number must have all numbers!"

        if (postData["cardexpiration"]) == "" or (postData["cardexpiration"]) == " ":
            errors["cardexpiration"] = "Expiration date cannot be empty!"

        expiration_date = datetime.strptime(postData["cardexpiration"], "%Y-%m-%d")
        if (expiration_date < now):
            errors["cardexpiration"] = "Expiration date must be in the future!"

        if not (postData["cardcvv"]).isnumeric():
            errors["cardcvv"] = "Card Code must have all numbers!"

        if len(postData["cardcvv"]) != 3:
            errors["cardcvv"] = "Card code must be a 3 digit code!"

        return errors

# Create your models here.
class Users(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Users_Manager()


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # default is what image you want to show
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Orders(models.Model):
    quantity = models.IntegerField()
    customer = models.ForeignKey(Users,related_name="orders_of_user",on_delete = models.CASCADE)
    product = models.ManyToManyField(Products,related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Card(models.Model):
    name = models.CharField(max_length=255)
    card_number = models.IntegerField()
    expiration = models.DateTimeField()
    card_code = models.IntegerField()
    owner = models.ForeignKey(Users,related_name="cards_of_user",on_delete = models.CASCADE)
    objects = Cards_Manager()

