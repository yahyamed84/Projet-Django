from django.views.generic import TemplateView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from .models import (
    Wilaya, FamilleProduit, Produit, PointVente, PrixProduit, ProduitPanier, INPC
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
        points_vente = PointVente.objects.select_related('commune__moughataa__wilaya').all()
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
        for point in points_vente:
            points_vente_data.append({
                'id': point.id,
                'nom': point.nom,
                'lat': float(point.latitude),
                'lng': float(point.longitude),
                'adresse': point.commune.nom,
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
        prix_qs = prix_qs.filter(point_vente__commune__moughataa__wilaya_id=wilaya_id)
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
    points_vente = PointVente.objects.select_related('commune__moughataa__wilaya').all()
    if wilaya_id:
        points_vente = points_vente.filter(commune__moughataa__wilaya_id=wilaya_id)
    
    points_data = [{
        'nom': p.nom,
        'latitude': float(p.latitude),
        'longitude': float(p.longitude),
        'adresse': p.commune.nom,
        'wilaya': p.commune.moughataa.wilaya.nom
    } for p in points_vente]
    
    return JsonResponse({
        'dates': dates,
        'prix_moyens': prix_moyens,
        'wilayas': wilayas,
        'prix_par_wilaya': prix_wilaya,
        'points_vente': points_data
    })

class INPCHomeView(TemplateView):
    template_name = 'core/inpc_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les 4 derniers mois d'INPC
        context['inpc_list'] = INPC.objects.order_by('-mois')[:4]
        
        # Si nous n'avons pas d'INPC pour le mois en cours, le calculer
        mois_actuel = timezone.now().date().replace(day=1)
        if not INPC.objects.filter(mois=mois_actuel).exists():
            try:
                INPC.calculer_inpc(mois_actuel)
                # Rafraîchir la liste après le calcul
                context['inpc_list'] = INPC.objects.order_by('-mois')[:4]
            except Exception as e:
                context['error_message'] = str(e)
        
        # Ajouter les années et mois pour le formulaire de calcul
        annee_courante = timezone.now().year
        context['annees'] = list(range(annee_courante, annee_courante - 5, -1))
        context['mois'] = [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'),
            (4, 'Avril'), (5, 'Mai'), (6, 'Juin'),
            (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'),
            (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]
            
        return context

    def post(self, request, *args, **kwargs):
        try:
            annee = int(request.POST.get('annee'))
            mois = int(request.POST.get('mois'))
            date_calcul = timezone.datetime(annee, mois, 1).date()
            
            inpc = INPC.calculer_inpc(date_calcul)
            
            return JsonResponse({
                'success': True,
                'mois': date_calcul.strftime('%B %Y'),
                'valeur': float(inpc.valeur)
            })
            
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f"Une erreur s'est produite lors du calcul : {str(e)}"
            })

@staff_member_required
def calculer_inpc_mois(request):
    """Vue pour calculer l'INPC d'un mois spécifique"""
    try:
        annee = int(request.POST.get('annee'))
        mois = int(request.POST.get('mois'))
        date_calcul = datetime(annee, mois, 1).date()
        
        inpc = INPC.calculer_inpc(date_calcul)
        return JsonResponse({
            'success': True,
            'mois': inpc.mois.strftime('%B %Y'),
            'valeur': float(inpc.valeur)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@method_decorator(staff_member_required, name='dispatch')
class ProduitPanierCreateView(CreateView):
    model = ProduitPanier
    fields = ['produit', 'ponderation', 'date_debut', 'date_fin']
    template_name = 'core/produit_panier_form.html'
    success_url = reverse_lazy('admin:core_produitpanier_changelist')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
