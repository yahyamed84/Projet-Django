from django import forms
from .models import ProductFamily, Cart, Product, CartProduct, ProductPrice, PointOfSale, Wilaya, Moughataa, Commune

# Formulaire pour les familles de produits
class ProductFamilyForm(forms.ModelForm):
    class Meta:
        model = ProductFamily
        fields = ['label']
        labels = {
            'label': 'Nom de la famille',
        }
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la famille',
                'maxlength': 255,
            }),
        }


# Formulaire pour les produits
# Formulaire pour les produits
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'unit_measure', 'product_family']  # Remplacer 'product_type' par 'product_family'
        labels = {
            'code': 'Code produit',
            'name': 'Nom du produit',
            'description': 'Description',
            'unit_measure': 'Unité de mesure',
            'product_family': 'Famille de produit',  # Utiliser le bon nom de champ
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code produit'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'unit_measure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unité de mesure'}),
            'product_family': forms.Select(attrs={'class': 'form-control'}),  # Dropdown pour sélectionner la famille de produit
        }



# Formulaire pour les paniers
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['code', 'name', 'description']
        labels = {
            'code': 'Code du panier',
            'name': 'Nom du panier',
            'description': 'Description du panier',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code du panier'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du panier'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# Formulaire pour les wilayas
class WilayaForm(forms.ModelForm):
    class Meta:
        model = Wilaya
        fields = ['name']
        labels = {
            'name': 'Nom de la Wilaya',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la Wilaya',
                'maxlength': 100,
            }),
        }


# Formulaire pour les moughataas
class MoughataaForm(forms.ModelForm):
    class Meta:
        model = Moughataa
        fields = ['label', 'code', 'wilaya']  # Adjust to use correct fields for Moughataa
        labels = {
            'label': 'Libellé de la Moughataa',
            'code': 'Code de la Moughataa',
            'wilaya': 'Wilaya associée',
        }
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Libellé de la Moughataa'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code de la Moughataa'}),
            'wilaya': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting Wilaya
        }


# Formulaire pour les communes
class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ['name', 'moughataa']
        labels = {
            'name': 'Nom de la Commune',
            'moughataa': 'Moughataa associée',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la Commune',
                'maxlength': 100,
            }),
            'moughataa': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting Moughataa
        }


# Formulaire pour les points de vente
class PointOfSaleForm(forms.ModelForm):
    class Meta:
        model = PointOfSale
        fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
        labels = {
            'code': 'Code du point de vente',
            'type': 'Type de point de vente',
            'gps_lat': 'Latitude',
            'gps_lon': 'Longitude',
            'commune': 'Commune associée',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code du point de vente'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type de point de vente'}),
            'gps_lat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'gps_lon': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
            'commune': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting Commune
        }


# Formulaire pour les prix des produits
class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = ['product', 'point_of_sale', 'value']  # Use 'value' instead of 'price'
        labels = {
            'product': 'Produit',
            'point_of_sale': 'Point de vente',
            'value': 'Prix',  # Adjust the field name if necessary
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'point_of_sale': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix'}),
        }


# Formulaire pour les produits dans un panier
class CartProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ['product', 'cart', 'weight']  # Adjusted to use 'cart' and 'weight'
        labels = {
            'product': 'Produit',
            'cart': 'Panier',
            'weight': 'Poids',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Poids'}),
        }
