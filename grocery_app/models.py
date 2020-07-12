import bcrypt, re
from django.db import models

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




# Create your models here.
class Users(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Users_Manager()

class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    # user can have many products
    customer = models.ForeignKey(Users,related_name="products_of_user",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

