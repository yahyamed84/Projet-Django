from django.urls import path
from .views import DashboardView, dashboard_data, ProduitPanierCreateView

app_name = 'core'

urlpatterns = [
    path('admin/dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('admin/dashboard/data/', dashboard_data, name='dashboard_data'),
    path('admin/panier/ajouter-produit/', ProduitPanierCreateView.as_view(), name='ajouter_produit_panier'),
]
