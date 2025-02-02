from django.views.generic import TemplateView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Avg, Q, Sum, Max
from django.utils import timezone
from datetime import timedelta, datetime
from .models import (
    Wilaya, FamilleProduit, Produit, PointVente, PrixProduit, ProduitPanier, INPC
)
from .forms import PointVenteForm
import json
import plotly.graph_objects as go
import plotly.express as px
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView

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

@staff_member_required
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

@method_decorator(staff_member_required, name='dispatch')
class INPCHomeView(TemplateView):
    template_name = 'core/inpc_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ajouter les années et mois pour le formulaire
        current_year = timezone.now().year
        context['years'] = range(current_year - 5, current_year + 1)
        context['months'] = [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'),
            (4, 'Avril'), (5, 'Mai'), (6, 'Juin'),
            (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'),
            (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]
        
        # Récupérer les 4 derniers INPC uniques par mois
        latest_inpcs = INPC.objects.values('mois').annotate(
            max_id=Max('id'),
            latest_valeur=Max('valeur'),
            latest_date=Max('date_calcul')
        ).order_by('-mois')[:4]
        
        context['inpc_list'] = [
            {
                'mois': item['mois'],
                'valeur': item['latest_valeur'],
                'date_calcul': item['latest_date']
            } for item in latest_inpcs
        ]
        
        # Récupérer les données INPC des 12 derniers mois
        last_12_months = timezone.now() - timedelta(days=365)
        inpc_data = INPC.objects.filter(
            mois__gte=last_12_months
        ).values('mois').annotate(
            valeur=Max('valeur')
        ).order_by('mois')

        # Line Chart - Evolution de l'INPC
        line_chart = go.Figure()
        line_chart.add_trace(go.Scatter(
            x=[item['mois'] for item in inpc_data],
            y=[item['valeur'] for item in inpc_data],
            mode='lines+markers',
            name='INPC'
        ))
        line_chart.update_layout(
            title='Evolution de l\'INPC sur 12 mois',
            xaxis_title='Mois',
            yaxis_title='Valeur INPC',
            template='plotly_white'
        )
        
        # Bar Chart - INPC par mois
        bar_data = INPC.objects.values('mois').annotate(
            avg_value=Max('valeur')
        ).order_by('-mois')[:6]
        
        bar_chart = go.Figure()
        bar_chart.add_trace(go.Bar(
            x=[item['mois'].strftime('%B %Y') for item in bar_data],
            y=[item['avg_value'] for item in bar_data],
            name='INPC Mensuel'
        ))
        bar_chart.update_layout(
            title='INPC Moyen par Mois',
            xaxis_title='Mois',
            yaxis_title='INPC Moyen',
            template='plotly_white'
        )

        # Pie Chart - Répartition par Famille de Produits
        produits_data = ProduitPanier.objects.values(
            'produit__famille__nom'
        ).annotate(
            total_ponderation=Sum('ponderation')
        ).order_by('-total_ponderation')

        pie_chart = go.Figure(data=[go.Pie(
            labels=[item['produit__famille__nom'] for item in produits_data],
            values=[item['total_ponderation'] for item in produits_data],
            hole=.3
        )])
        pie_chart.update_layout(
            title='Répartition des Pondérations par Famille de Produits',
            template='plotly_white'
        )

        # Convert charts to HTML
        context['line_chart'] = line_chart.to_html(full_html=False)
        context['bar_chart'] = bar_chart.to_html(full_html=False)
        context['pie_chart'] = pie_chart.to_html(full_html=False)
        
        return context

    def post(self, request, *args, **kwargs):
        try:
            year = int(request.POST.get('year'))
            month = int(request.POST.get('month'))
            date = datetime(year, month, 1).date()
            
            inpc = INPC.calculer_inpc(date)
            return JsonResponse({
                'success': True,
                'inpc': {
                    'mois': inpc.mois.strftime('%B %Y'),
                    'valeur': float(inpc.valeur),
                    'date_calcul': inpc.date_calcul.strftime('%d/%m/%Y')
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

@login_required
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

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    success_url = '/admin/'
    
    def get_success_url(self):
        return self.success_url

@method_decorator(staff_member_required, name='dispatch')
class ProduitPanierCreateView(CreateView):
    model = ProduitPanier
    fields = ['produit', 'ponderation', 'date_debut', 'date_fin']
    template_name = 'core/produit_panier_form.html'
    success_url = reverse_lazy('admin:core_produitpanier_changelist')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
