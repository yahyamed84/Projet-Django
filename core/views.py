from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Wilaya, FamilleProduit, Produit,
    PointVente, PrixProduit, ProduitPanier, PanierProduits
)
from .forms import PointVenteForm
import json

# Create your views here.

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les filtres
        wilaya_id = self.request.GET.get('wilaya')
        periode = self.request.GET.get('periode', '7')
        famille_id = self.request.GET.get('famille')

        # Base des requêtes avec filtres
        prix_base = PrixProduit.objects.filter(
            date_releve__gte=timezone.now() - timedelta(days=int(periode))
        )
        points_vente = PointVente.objects.all()
        produits = Produit.objects.all()

        # Appliquer les filtres
        if wilaya_id and wilaya_id != 'all':
            points_vente = points_vente.filter(commune__moughataa__wilaya_id=wilaya_id)
            prix_base = prix_base.filter(point_vente__commune__moughataa__wilaya_id=wilaya_id)
            produit_ids = prix_base.values_list('produit_id', flat=True).distinct()
            produits = produits.filter(id__in=produit_ids)

        if famille_id and famille_id != 'all':
            produits = produits.filter(famille_id=famille_id)
            prix_base = prix_base.filter(produit__famille_id=famille_id)
            point_vente_ids = prix_base.values_list('point_vente_id', flat=True).distinct()
            points_vente = points_vente.filter(id__in=point_vente_ids)

        # Préparer les données des points de vente pour la carte
        points_vente_data = []
        for point in points_vente.select_related('commune__moughataa__wilaya'):
            points_vente_data.append({
                'id': point.id,
                'nom': point.nom,
                'lat': float(point.latitude),  # Convertir en float pour JSON
                'lng': float(point.longitude),  # Convertir en float pour JSON
                'adresse': point.adresse,
                'commune': point.commune.nom,
                'moughataa': point.commune.moughataa.nom,
                'wilaya': point.commune.moughataa.wilaya.nom,
                'prix_count': prix_base.filter(point_vente=point).count()
            })

        # Compter les prix d'aujourd'hui
        prix_aujourdhui = prix_base.filter(date_releve__date=timezone.now().date())

        # Préparer le contexte
        context.update({
            'points_vente_count': points_vente.count(),
            'produits_count': produits.count(),
            'prix_count': prix_base.count(),
            'prix_aujourdhui_count': prix_aujourdhui.count(),
            'points_vente_json': json.dumps(points_vente_data),
            'wilayas': Wilaya.objects.all(),
            'familles': FamilleProduit.objects.all(),
            'selected_wilaya': wilaya_id,
            'selected_periode': periode,
            'selected_famille': famille_id
        })

        return context

def dashboard_data(request):
    # Récupération des filtres
    wilaya_id = request.GET.get('wilaya')
    periode = int(request.GET.get('periode', 30))
    famille_id = request.GET.get('famille')
    
    # Date de début pour la période
    date_debut = timezone.now() - timedelta(days=periode)
    
    # Base des requêtes
    prix_qs = PrixProduit.objects.filter(date_releve__gte=date_debut)
    
    # Application des filtres
    if wilaya_id:
        prix_qs = prix_qs.filter(
            point_vente__commune__moughataa__wilaya_id=wilaya_id
        )
    if famille_id:
        prix_qs = prix_qs.filter(produit__famille_id=famille_id)
    
    # Données pour le graphique d'évolution des prix
    prix_par_jour = prix_qs.values('date_releve__date').annotate(
        prix_moyen=Avg('prix')
    ).order_by('date_releve__date')
    
    dates = [p['date_releve__date'].strftime('%Y-%m-%d') for p in prix_par_jour]
    prix_moyens = [float(p['prix_moyen']) for p in prix_par_jour]
    
    # Données pour le graphique par wilaya
    prix_par_wilaya = prix_qs.values(
        'point_vente__commune__moughataa__wilaya__nom'
    ).annotate(
        prix_moyen=Avg('prix')
    ).order_by('point_vente__commune__moughataa__wilaya__nom')
    
    wilayas = [p['point_vente__commune__moughataa__wilaya__nom'] for p in prix_par_wilaya]
    prix_wilaya = [float(p['prix_moyen']) for p in prix_par_wilaya]
    
    # Données pour la carte
    points_vente = PointVente.objects.all()
    if wilaya_id:
        points_vente = points_vente.filter(
            commune__moughataa__wilaya_id=wilaya_id
        )
    
    points_data = [{
        'nom': p.nom,
        'latitude': float(p.latitude),  # Convertir en float pour JSON
        'longitude': float(p.longitude),  # Convertir en float pour JSON
        'adresse': p.adresse,
        'commune': str(p.commune)
    } for p in points_vente]
    
    return JsonResponse({
        'dates': dates,
        'prix_moyens': prix_moyens,
        'wilayas': wilayas,
        'prix_par_wilaya': prix_wilaya,
        'points_vente': points_data
    })

@method_decorator(staff_member_required, name='dispatch')
class ProduitPanierCreateView(CreateView):
    model = ProduitPanier
    template_name = 'core/produit_panier_form.html'
    success_url = reverse_lazy('admin:core_panierproduits_changelist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter un produit au panier'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
