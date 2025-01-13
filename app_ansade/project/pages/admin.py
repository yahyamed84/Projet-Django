from django.contrib import admin
from .models import Product, ProductFamily, Cart

@admin.register(ProductFamily)
class ProductFamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')  # Affiche l'ID et le label de la famille
    search_fields = ('label',)  # Ajout de la recherche par label
    ordering = ('id',)  # Tri par ID
    readonly_fields = ('id',)  # ID en lecture seule

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'product_family', 'unit_measure')  # Remplacer 'price_unit' par 'unit_measure'
    search_fields = ('name', 'code')  # Recherche par name et code
    list_filter = ('product_family',)  # Remplacer 'product_type' par 'product_family'
    ordering = ('id',)  # Tri par ID
    list_per_page = 20  # Pagination dans l'interface admin
    readonly_fields = ('id',)  # ID en lecture seule

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')  # Remplacer 'label' par 'name'
    search_fields = ('name', 'code')  # Recherche par name et code
    ordering = ('id',)  # Tri par ID
    readonly_fields = ('id',)  # ID en lecture seule
