from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Avg
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .views import DashboardView, dashboard_data
from .models import (
    Wilaya, Moughataa, Commune,
    FamilleProduit, Produit,
    PanierProduits, ProduitPanier,
    PointVente, PrixProduit, INPC
)
from .forms import PointVenteForm
from django.contrib import messages

class CustomAdminSite(AdminSite):
    site_header = 'Administration des données INPC'
    site_title = 'Administration INPC'
    index_title = 'GESTION INPC'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return app_list
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(DashboardView.as_view()), name='dashboard'),
            path('dashboard/data/', self.admin_view(dashboard_data), name='dashboard_data'),
        ]
        return custom_urls + urls

admin_site = CustomAdminSite(name='admin')

# Resources pour l'export Excel
class WilayaResource(resources.ModelResource):
    class Meta:
        model = Wilaya
        fields = ('id', 'nom', 'code')

class MoughataaResource(resources.ModelResource):
    class Meta:
        model = Moughataa
        fields = ('id', 'nom', 'code', 'wilaya__nom')

class CommuneResource(resources.ModelResource):
    class Meta:
        model = Commune
        fields = ('id', 'nom', 'code', 'moughataa__nom', 'moughataa__wilaya__nom')

class ProduitResource(resources.ModelResource):
    class Meta:
        model = Produit
        fields = ('id', 'code', 'nom', 'description', 'unite_mesure', 'famille__nom')

class PrixProduitResource(resources.ModelResource):
    class Meta:
        model = PrixProduit
        fields = ('id', 'produit__nom', 'point_vente__nom', 'prix', 'date_releve', 'date_saisie')

@admin.register(Wilaya, site=admin_site)
class WilayaAdmin(ImportExportModelAdmin):
    resource_class = WilayaResource
    list_display = ('nom', 'code', 'get_moughataas_count')
    search_fields = ('nom', 'code')
    ordering = ('nom',)

    def get_moughataas_count(self, obj):
        return obj.moughataas.count()
    get_moughataas_count.short_description = 'Nombre de Moughataas'

@admin.register(Moughataa, site=admin_site)
class MoughataaAdmin(ImportExportModelAdmin):
    resource_class = MoughataaResource
    list_display = ('nom', 'code', 'wilaya', 'get_communes_count')
    list_filter = ('wilaya',)
    search_fields = ('nom', 'code', 'wilaya__nom')
    ordering = ('wilaya', 'nom')
    autocomplete_fields = ['wilaya']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('wilaya')

    def get_communes_count(self, obj):
        return obj.communes.count()
    get_communes_count.short_description = 'Nombre de Communes'

@admin.register(Commune, site=admin_site)
class CommuneAdmin(ImportExportModelAdmin):
    resource_class = CommuneResource
    list_display = ('nom', 'code', 'moughataa', 'wilaya_display', 'get_points_vente_count')
    list_filter = ('moughataa__wilaya', 'moughataa')
    search_fields = ('nom', 'code', 'moughataa__nom', 'moughataa__wilaya__nom')
    ordering = ('moughataa', 'nom')
    autocomplete_fields = ['moughataa']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('moughataa', 'moughataa__wilaya')

    def wilaya_display(self, obj):
        return obj.moughataa.wilaya
    wilaya_display.short_description = 'Wilaya'

    def get_points_vente_count(self, obj):
        return obj.points_vente.count()
    get_points_vente_count.short_description = 'Points de vente'

@admin.register(FamilleProduit, site=admin_site)
class FamilleProduitAdmin(ImportExportModelAdmin):
    list_display = ('nom', 'code', 'get_produits_count')
    search_fields = ('nom', 'code')
    ordering = ('nom',)

    def get_produits_count(self, obj):
        return obj.produits.count()
    get_produits_count.short_description = 'Nombre de produits'

@admin.register(Produit, site=admin_site)
class ProduitAdmin(ImportExportModelAdmin):
    resource_class = ProduitResource
    list_display = ('code', 'nom', 'unite_mesure', 'famille', 'get_prix_moyen')
    list_filter = ('famille',)
    search_fields = ('nom', 'code', 'famille__nom')
    ordering = ('famille', 'nom')
    autocomplete_fields = ['famille']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('famille')

    def get_prix_moyen(self, obj):
        prix_moyen = obj.prix.aggregate(Avg('prix'))['prix__avg']
        return round(prix_moyen, 2) if prix_moyen else None
    get_prix_moyen.short_description = 'Prix moyen'

class ProduitPanierInline(admin.TabularInline):
    model = ProduitPanier
    extra = 1
    fields = ['produit', 'ponderation', 'date_debut', 'date_fin']

@admin.register(PanierProduits, site=admin_site)
class PanierProduitsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation', 'get_produits_count')
    search_fields = ('nom',)
    inlines = [ProduitPanierInline]
    
    def get_produits_count(self, obj):
        return obj.produits.count()
    get_produits_count.short_description = 'Nombre de produits'

@admin.register(ProduitPanier, site=admin_site)
class ProduitPanierAdmin(admin.ModelAdmin):
    list_display = ('produit', 'panier', 'ponderation', 'date_debut', 'date_fin')
    list_filter = ('panier', 'produit', 'date_debut')
    search_fields = ('produit__nom', 'panier__nom')
    date_hierarchy = 'date_debut'

@admin.register(PointVente, site=admin_site)
class PointVenteAdmin(ImportExportModelAdmin):
    form = PointVenteForm
    list_display = ('nom', 'commune', 'get_coordinates', 'date_creation')
    list_filter = ('commune__moughataa__wilaya', 'commune__moughataa', 'commune')
    search_fields = ('nom', 'adresse')
    fields = ('nom', 'commune', 'latitude', 'longitude', 'adresse')
    
    def get_coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return f"{obj.latitude}, {obj.longitude}"
        return "Non spécifié"
    get_coordinates.short_description = "Coordonnées"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'commune',
            'commune__moughataa',
            'commune__moughataa__wilaya'
        )

    def get_prix_count(self, obj):
        return obj.prix.count()
    get_prix_count.short_description = 'Nombre de prix'

@admin.register(PrixProduit, site=admin_site)
class PrixProduitAdmin(ImportExportModelAdmin):
    resource_class = PrixProduitResource
    list_display = ('produit', 'point_vente', 'prix', 'date_releve', 'statut')
    list_filter = ('statut', 'date_releve', 'point_vente__commune__moughataa__wilaya')
    search_fields = ('produit__nom', 'point_vente__nom')
    date_hierarchy = 'date_releve'
    readonly_fields = ('date_saisie',)
    
    def save_model(self, request, obj, form, change):
        """
        Surcharge de la méthode de sauvegarde pour gérer le recalcul de l'INPC
        """
        # Sauvegarder le statut actuel avant modification
        ancien_statut = None
        if change:  # Si c'est une modification
            ancien_obj = self.model.objects.get(pk=obj.pk)
            ancien_statut = ancien_obj.statut

        # Sauvegarder l'objet
        super().save_model(request, obj, form, change)

        # Si le statut passe à 'validé', recalculer l'INPC
        if obj.statut == 'validé' and ancien_statut != 'validé':
            mois_prix = obj.date_releve.date().replace(day=1)
            try:
                # Supprimer l'ancien INPC pour ce mois
                INPC.objects.filter(mois=mois_prix).delete()
                # Recalculer l'INPC
                INPC.calculer_inpc(mois_prix)
                self.message_user(
                    request,
                    f"L'INPC a été recalculé pour le mois de {mois_prix.strftime('%B %Y')}",
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Erreur lors du recalcul de l'INPC : {str(e)}",
                    messages.ERROR
                )

# Template personnalisé pour la page d'accueil
admin_site.index_template = 'admin/custom_index.html'
