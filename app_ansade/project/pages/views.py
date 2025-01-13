from django.shortcuts import render, redirect, get_object_or_404
# Mise à jour des importations après les derniers ajouts
from .models import ProductFamily, Cart, Product, CartProduct, ProductPrice, PointOfSale, Wilaya, Moughataa, Commune
from .forms import (
    ProductFamilyForm, ProductForm, CartForm, CartProductForm,
    ProductPriceForm, PointOfSaleForm, WilayaForm, MoughataaForm, CommuneForm
)

# Vue pour la page d'accueil
def home(request):
    return render(request, 'pages/home.html')


# ------------------- Gestion des Familles de Produits -------------------
def product_family_list(request):
    families = ProductFamily.objects.all()
    return render(request, 'pages/product_family_list.html', {'families': families})

def product_family_create(request):
    form = ProductFamilyForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_family_list')
    return render(request, 'pages/product_family_form.html', {'form': form})

def product_family_update(request, pk):
    family = get_object_or_404(ProductFamily, pk=pk)
    form = ProductFamilyForm(request.POST or None, instance=family)
    if form.is_valid():
        form.save()
        return redirect('product_family_list')
    return render(request, 'pages/product_family_form.html', {'form': form})

def product_family_delete(request, pk):
    family = get_object_or_404(ProductFamily, pk=pk)
    if request.method == 'POST':
        family.delete()
        return redirect('product_family_list')
    return render(request, 'pages/product_family_confirm_delete.html', {'family': family})


# ------------------- Gestion des Produits -------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, 'pages/produit/product_list.html', {'products': products})

def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'pages/produit/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'pages/produit/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'pages/produit/product_confirm_delete.html', {'product': product})


# ------------------- Gestion des Paniers -------------------
def panier_list(request):
    carts = Cart.objects.all()
    return render(request, 'pages/paniers/panier_list.html', {'carts': carts})

def panier_create(request):
    form = CartForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('panier_list')
    return render(request, 'pages/paniers/panier_create.html', {'form': form})

def panier_update(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    form = CartForm(request.POST or None, instance=cart)
    if form.is_valid():
        form.save()
        return redirect('pages/panier_list')
    return render(request, 'paniers/panier_form.html', {'form': form})

def panier_delete(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        cart.delete()
        return redirect('panier_list')
    return render(request, 'pages/paniers/panier_confirm_delete.html', {'cart': cart})


# ------------------- Gestion des Produits dans les Paniers -------------------
def product_cart_list(request):
    cart_products = CartProduct.objects.all()
    return render(request, 'pages/product_cart/product_cart_list.html', {'cart_products': cart_products})

def product_cart_create(request):
    form = CartProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_cart_list')
    return render(request, 'pages/product_cart/product_cart_create.html', {'form': form})

def product_cart_update(request, pk):
    cart_product = get_object_or_404(CartProduct, pk=pk)
    form = CartProductForm(request.POST or None, instance=cart_product)
    if form.is_valid():
        form.save()
        return redirect('product_cart_list')
    return render(request, 'pages/product_cart/product_cart_form.html', {'form': form})

def product_cart_delete(request, pk):
    cart_product = get_object_or_404(CartProduct, pk=pk)
    if request.method == 'POST':
        cart_product.delete()
        return redirect('product_cart_list')
    return render(request, 'pages/product_cart/product_cart_confirm_delete.html', {'cart_product': cart_product})


# ------------------- Gestion des Prix des Produits -------------------
def product_price_list(request):
    product_prices = ProductPrice.objects.all()
    return render(request, 'pages/product_price/product_price_list.html', {'product_prices': product_prices})

def product_price_create(request):
    form = ProductPriceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_price_list')
    return render(request, 'pages/product_price/product_price_create.html', {'form': form})

def product_price_update(request, pk):
    product_price = get_object_or_404(ProductPrice, pk=pk)
    form = ProductPriceForm(request.POST or None, instance=product_price)
    if form.is_valid():
        form.save()
        return redirect('product_price_list')
    return render(request, 'pages/product_price/product_price_form.html', {'form': form})

def product_price_delete(request, pk):
    product_price = get_object_or_404(ProductPrice, pk=pk)
    if request.method == 'POST':
        product_price.delete()
        return redirect('product_price_list')
    return render(request, 'pages/product_price/product_price_confirm_delete.html', {'product_price': product_price})


# ------------------- Gestion des Points de Vente -------------------
def point_of_sale_list(request):
    points_of_sales = PointOfSale.objects.all()
    return render(request, 'pages/point_of_sale/point_of_sale_list.html', {'points_of_sales': points_of_sales})

def point_of_sale_create(request):
    form = PointOfSaleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('point_of_sale_list')
    return render(request, 'pages/point_of_sale/point_of_sale_create.html', {'form': form})

def point_of_sale_update(request, pk):
    point_of_sale = get_object_or_404(PointOfSale, pk=pk)
    form = PointOfSaleForm(request.POST or None, instance=point_of_sale)
    if form.is_valid():
        form.save()
        return redirect('point_of_sale_list')
    return render(request, 'pages/point_of_sale/point_of_sale_form.html', {'form': form})

def point_of_sale_delete(request, pk):
    point_of_sale = get_object_or_404(PointOfSale, pk=pk)
    if request.method == 'POST':
        point_of_sale.delete()
        return redirect('point_of_sale_list')
    return render(request, 'pages/point_of_sale/point_of_sale_confirm_delete.html', {'point_of_sale': point_of_sale})


# ------------------- Gestion des Wilayas -------------------
def wilaya_list(request):
    wilayas = Wilaya.objects.all()
    return render(request, 'pages/wilaya/wilaya_list.html', {'wilayas': wilayas})

def wilaya_create(request):
    form = WilayaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('wilaya_list')
    return render(request, 'pages/wilaya/wilaya_create.html', {'form': form})

def wilaya_update(request, pk):
    wilaya = get_object_or_404(Wilaya, pk=pk)
    form = WilayaForm(request.POST or None, instance=wilaya)
    if form.is_valid():
        form.save()
        return redirect('wilaya_list')
    return render(request, 'pages/wilaya/wilaya_form.html', {'form': form})

def wilaya_delete(request, pk):
    wilaya = get_object_or_404(Wilaya, pk=pk)
    if request.method == 'POST':
        wilaya.delete()
        return redirect('wilaya_list')
    return render(request, 'pages/wilaya/wilaya_confirm_delete.html', {'wilaya': wilaya})


# ------------------- Gestion des Moughataas -------------------
def moughataa_list(request):
    moughataas = Moughataa.objects.all()
    return render(request, 'pages/moughataa/moughataa_list.html', {'moughataas': moughataas})

def moughataa_create(request):
    form = MoughataaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('moughataa_list')
    return render(request, 'pages/moughataa/moughataa_create.html', {'form': form})

def moughataa_update(request, pk):
    moughataa = get_object_or_404(Moughataa, pk=pk)
    form = MoughataaForm(request.POST or None, instance=moughataa)
    if form.is_valid():
        form.save()
        return redirect('moughataa_list')
    return render(request, 'pages/moughataa/moughataa_form.html', {'form': form})

def moughataa_delete(request, pk):
    moughataa = get_object_or_404(Moughataa, pk=pk)
    if request.method == 'POST':
        moughataa.delete()
        return redirect('moughataa_list')
    return render(request, 'pages/moughataa/moughataa_confirm_delete.html', {'moughataa': moughataa})


# ------------------- Gestion des Communes -------------------
def commune_list(request):
    communes = Commune.objects.all()
    return render(request, 'pages/commune/commune_list.html', {'communes': communes})

def commune_create(request):
    form = CommuneForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('commune_list')
    return render(request, 'pages/commune/commune_create.html', {'form': form})

def commune_update(request, pk):
    commune = get_object_or_404(Commune, pk=pk)
    form = CommuneForm(request.POST or None, instance=commune)
    if form.is_valid():
        form.save()
        return redirect('commune_list')
    return render(request, 'pages/commune/commune_form.html', {'form': form})

def commune_delete(request, pk):
    commune = get_object_or_404(Commune, pk=pk)
    if request.method == 'POST':
        commune.delete()
        return redirect('commune_list')
    return render(request, 'pages/commune/commune_confirm_delete.html', {'commune': commune})
