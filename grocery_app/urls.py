from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('register', views.add_account),
    path('login', views.login),
    path('welcome', views.welcome_page),
    ### add products to checkout page
    path('product/add', views.add_product)
    # path('noorani/checkout', views.checkout),
    # path('logout', views.logout),
    # path('delete/<int:id>', views.delete_product),
    ### page below renders web page to add account info
    # path('noorani/account', views.account_info)
    # path('account/update', views.update_account)


]