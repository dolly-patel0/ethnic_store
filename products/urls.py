from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('category/<str:category>/', views.product_list_view, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
]