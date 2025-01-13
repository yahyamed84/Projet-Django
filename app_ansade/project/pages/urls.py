from django.urls import path
from . import views  # Import des vues de l'application "pages"

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),

    # Gestion des familles de produits
    path('families/', views.product_family_list, name='product_family_list'),
    path('families/create/', views.product_family_create, name='product_family_create'),
    path('families/update/<int:pk>/', views.product_family_update, name='product_family_update'),
    path('families/delete/<int:pk>/', views.product_family_delete, name='product_family_delete'),

    # Gestion des produits
    path('produits/', views.product_list, name='product_list'),
    path('produits/create/', views.product_create, name='product_create'),
    path('produits/update/<int:pk>/', views.product_update, name='product_update'),
    path('produits/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Gestion des paniers
    path('paniers/', views.panier_list, name='panier_list'),
    path('paniers/create/', views.panier_create, name='panier_create'),
    path('paniers/update/<int:pk>/', views.panier_update, name='panier_update'),
    path('paniers/delete/<int:pk>/', views.panier_delete, name='panier_delete'),

    # Gestion des produits liés aux paniers
    path('product-cart/', views.product_cart_list, name='product_cart_list'),
    path('product-cart/create/', views.product_cart_create, name='product_cart_create'),
    path('product-cart/update/<int:pk>/', views.product_cart_update, name='product_cart_update'),
    path('product-cart/delete/<int:pk>/', views.product_cart_delete, name='product_cart_delete'),

    # Gestion des prix des produits
    path('product-price/', views.product_price_list, name='product_price_list'),
    path('product-price/create/', views.product_price_create, name='product_price_create'),
    path('product-price/update/<int:pk>/', views.product_price_update, name='product_price_update'),
    path('product-price/delete/<int:pk>/', views.product_price_delete, name='product_price_delete'),

    # Gestion des points de ventes
    path('point-of-sale/', views.point_of_sale_list, name='point_of_sale_list'),
    path('point-of-sale/create/', views.point_of_sale_create, name='point_of_sale_create'),
    path('point-of-sale/update/<int:pk>/', views.point_of_sale_update, name='point_of_sale_update'),
    path('point-of-sale/delete/<int:pk>/', views.point_of_sale_delete, name='point_of_sale_delete'),

    # Gestion des wilayas
    path('wilaya/', views.wilaya_list, name='wilaya_list'),
    path('wilaya/create/', views.wilaya_create, name='wilaya_create'),
    path('wilaya/update/<int:pk>/', views.wilaya_update, name='wilaya_update'),
    path('wilaya/delete/<int:pk>/', views.wilaya_delete, name='wilaya_delete'),

    # Gestion des moughataas
    path('moughataa/', views.moughataa_list, name='moughataa_list'),
    path('moughataa/create/', views.moughataa_create, name='moughataa_create'),
    path('moughataa/update/<int:pk>/', views.moughataa_update, name='moughataa_update'),
    path('moughataa/delete/<int:pk>/', views.moughataa_delete, name='moughataa_delete'),

    # Gestion des communes
    path('commune/', views.commune_list, name='commune_list'),
    path('commune/create/', views.commune_create, name='commune_create'),
    path('commune/update/<int:pk>/', views.commune_update, name='commune_update'),
    path('commune/delete/<int:pk>/', views.commune_delete, name='commune_delete'),
]
