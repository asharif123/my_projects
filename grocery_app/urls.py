from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# AJAX allows web pages to be updated by exchanging small amounts of information with the server without refreshing page.


urlpatterns = [
    path('home', views.main_page),
    path('', views.welcome_page),
    path('register', views.add_account),
    path('login', views.login),
    path('welcome', views.welcome_page),
    path('order/add', views.add_order),
    path('logout', views.logout),
    path('like/<int:id>', views.liked_product),
    path('unlike/<int:id>', views.unliked_product),
    path('noorani/checkout', views.checkout),
    path('delete/item', views.delete_product),
    path('noorani/delete/all', views.delete_all),
    path('noorani/account', views.account_page),
    path('noorani/success', views.success),
    path('noorani/favorites', views.favorites),
    path('account/info', views.account_info),
    path('noorani/account/update', views.update_account),
# USING STRIPE API
    path('charge', views.charge),
    path('noorani/checkout/page', views.checkout_page)


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

