from django.db import models


# ------------------- Modèle ProductFamily -------------------
class ProductFamily(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


# ------------------- Modèle Product -------------------
class Product(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    name = models.CharField(max_length=45, verbose_name="Nom", default="Nom du produit par défaut")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    unit_measure = models.CharField(
        max_length=45, blank=True, null=True, verbose_name="Unité de mesure"
    )
    product_family = models.ForeignKey(ProductFamily, on_delete=models.CASCADE, verbose_name="Famille de produit")

    def __str__(self):
        return self.name



# ------------------- Modèle Cart -------------------
class Cart(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    name = models.CharField(max_length=45, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name


# ------------------- Modèle CartProduct -------------------
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Panier")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    weight = models.FloatField(verbose_name="Poids")
    date_from = models.DateField(verbose_name="Date de début")
    date_to = models.DateField(verbose_name="Date de fin")

    def __str__(self):
        return f"{self.product.name} dans {self.cart.name}"


# ------------------- Modèle ProductPrice -------------------
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    value = models.FloatField(verbose_name="Prix")
    date_from = models.DateField(verbose_name="Date de début")
    date_to = models.DateField(verbose_name="Date de fin")
    point_of_sale = models.ForeignKey("PointOfSale", on_delete=models.CASCADE, verbose_name="Point de vente")

    def __str__(self):
        return f"{self.product.name} - {self.value} MRO"



# ------------------- Modèle PointOfSale -------------------
class PointOfSale(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    type = models.CharField(max_length=45, verbose_name="Type")
    gps_lat = models.FloatField(verbose_name="Latitude")
    gps_lon = models.FloatField(verbose_name="Longitude")
    commune = models.ForeignKey(
        "Commune", on_delete=models.CASCADE, verbose_name="Commune"
    )

    class Meta:
        verbose_name = "Point de vente"
        verbose_name_plural = "Points de vente"

    def __str__(self):
        return f"{self.code} ({self.type})"


# ------------------- Modèle Wilaya -------------------
class Wilaya(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    name = models.CharField(max_length=45, verbose_name="Nom")

    class Meta:
        verbose_name = "Wilaya"
        verbose_name_plural = "Wilayas"

    def __str__(self):
        return self.name


# ------------------- Modèle Moughataa -------------------
class Moughataa(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    label = models.CharField(max_length=45, verbose_name="Libellé")
    wilaya = models.ForeignKey(
        Wilaya, on_delete=models.CASCADE, verbose_name="Wilaya associée"
    )

    class Meta:
        verbose_name = "Moughataa"
        verbose_name_plural = "Moughataas"

    def __str__(self):
        return self.label


# ------------------- Modèle Commune -------------------
class Commune(models.Model):
    code = models.CharField(max_length=45, unique=True, verbose_name="Code")
    name = models.CharField(max_length=45, verbose_name="Nom")
    moughataa = models.ForeignKey(
        Moughataa, on_delete=models.CASCADE, verbose_name="Moughataa associée"
    )

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"

    def __str__(self):
        return self.name
