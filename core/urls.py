from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView, dashboard_data, ProduitPanierCreateView,
    INPCHomeView, calculer_inpc_mois, CustomLoginView
)

app_name = 'core'

urlpatterns = [
    path('', INPCHomeView.as_view(), name='home'),  # Nouvelle page d'accueil
    path('admin/dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('admin/dashboard/data/', dashboard_data, name='dashboard_data'),
    path('admin/panier/ajouter-produit/', ProduitPanierCreateView.as_view(), name='ajouter_produit_panier'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('calculer-inpc/', calculer_inpc_mois, name='calculer_inpc'),
]
