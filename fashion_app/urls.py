from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ethnic-wear/', views.ethnic_wear, name='ethnic_wear'),
    path('office-wear/', views.office_wear, name='office_wear'),
    path('tops-tunics/', views.tops_tunics, name='tops_tunics'),
    path('collections/', views.collections, name='collections'),
     path('contact/', views.contact, name='contact'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('profile/', views.profile, name='profile'),
    path('lookbook/', views.lookbook, name='lookbook'),
    path('faq/', views.faq, name='faq'),
    path('returns/', views.returns, name='returns'),
    path('shipping/', views.shipping, name='shipping'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-conditions/', views.terms, name='terms'),
]