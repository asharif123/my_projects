from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('register', views.add_account),
    path('login', views.login),
    path('welcome', views.welcome_page),
    path('product/add', views.add_product),
    path('logout', views.logout),
    path('noorani/checkout', views.checkout),
    path('delete/<int:id>', views.delete_product),
    path('noorani/delete/all', views.delete_all),
    path('noorani/account', views.account_page),
    path('noorani/submit', views.submit),
    path('noorani/success', views.success)
    # path('account/update', views.update_account),
    # path('payment/update', views.payment_update),
    # path('noorani/favorite', views.favorite_items)


]