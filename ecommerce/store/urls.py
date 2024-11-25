from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.login_view, name="login_view"),
    path('logout/',views.user_logout,name='logout'),
    path('signup/', views.signup_view, name='signup_view'), 
    path('search/', views.search_view, name='search_view'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:pk>/', views.product, name='product'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('', views.home, name='home'),
]
